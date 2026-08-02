package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/redis/go-redis/v9"
)

func main() {
	ctx := context.Background()

	redisURL := os.Getenv("REDIS_URL")
	dbURL := os.Getenv("DATABASE_URL")

	var rdb *redis.Client
	var conn *pgx.Conn
	var err error

	// Wait for Redis
	for {
		opts, parseErr := redis.ParseURL(redisURL)
		if parseErr != nil {
			panic(fmt.Sprintf("invalid REDIS_URL %q: %v", redisURL, parseErr))
		}
		rdb = redis.NewClient(opts)

		if err = rdb.Ping(ctx).Err(); err == nil {
			break
		}

		fmt.Println("Waiting for Redis...")
		time.Sleep(2 * time.Second)
	}

	// Wait for PostgreSQL
	for {
		conn, err = pgx.Connect(ctx, dbURL)

		if err == nil {
			break
		}

		fmt.Println("Waiting for PostgreSQL...")
		time.Sleep(2 * time.Second)
	}

	defer conn.Close(ctx)

	// If counter already exists, exit
	exists, err := rdb.Exists(ctx, "global:id").Result()
	if err != nil {
		panic(err)
	}

	if exists == 1 {
		fmt.Println("Counter already initialized.")
		return
	}

	var maxID int64

	err = conn.QueryRow(
		ctx,
		"SELECT COALESCE(MAX(id),0) FROM urls",
	).Scan(&maxID)

	if err != nil {
		// On a fresh database the urls table won't exist yet (it is created
		// by url-shortener-service on first startup). Treat this as 0.
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "42P01" {
			fmt.Println("Table 'urls' does not exist yet (fresh database). Initializing counter to 0.")
			maxID = 0
		} else {
			panic(err)
		}
	}

	err = rdb.Set(ctx, "global:id", maxID, 0).Err()

	if err != nil {
		panic(err)
	}

	fmt.Printf("Initialized counter to %d\n", maxID)
}