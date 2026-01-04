#!/bin/bash

# --- Configuration ---
# Define paths to your project directories and server commands
PROJECT_ROOT=$(pwd -P)
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT"
MESSAGES_DIR="$PROJECT_ROOT/messages"
KARAFKA_DIR="$PROJECT_ROOT/messages"
KAFKA_DIR="$PROJECT_ROOT/kafka-4.1.0-src"

# Server commands
FRONTEND_CMD="npm run dev" #Main React frontend
BACKEND_CMD="python manage.py runserver" #Django app
MESSAGES_CMD="rails server" #Rails message service
KARAFKA_CMD="bundle exec karafka server" #Karafka message server
KAFKA_CMD="sudo bin/kafka-server-start.sh config/server.properties" #Main Kafka Cluster
ENV_CMD="source activate"

#Terminal
TERMINAL_EMULATOR="gnome-terminal"

start_backend(){
        echo "Starting backend server..."
        cd "$BACKEND_DIR/../env/bin" || exit
	$ENV_CMD
        cd "$BACKEND_DIR" || exit
        $BACKEND_CMD &
       	BACKEND_PID=$!
        echo "Backend server started with PID: $BACKEND_PPID"
}

start_frontend() {
	echo "Starting frontend server..."
	cd "$FRONTEND_DIR" || exit
	$TERMINAL_EMULATOR -e "bash -c \"$FRONTEND_CMD & FRONTEND_PID=$!; exec bash\"" &
	echo "Frontend server started with PID: $FRONTEND_PPID"
}

start_messages() {
    echo "Starting messages microservice..."
    cd "$MESSAGES_DIR" || exit
    $TERMINAL_EMULATOR -e "bash -c \"$MESSAGES_CMD & MESSAGES_PID=$!; exec bash\"" &
    echo "Messages server started with PID: $MESSAGES_PID"
}

start_karafka() {
    echo "Starting messages karafka server..."
    cd "$KARAFKA_DIR" || exit
    $TERMINAL_EMULATOR -e "bash -c \"$KARAFKA_CMD & KARAFKA_PID=$!; exec bash\"" &
    echo "Karafka server started with PID: $KARAFKA_PID"
}

start_kafka() {
    echo "Starting main kafka cluster..."
    cd "$KAFKA_DIR" || exit
    $TERMINAL_EMULATOR -e "bash -c \"$KAFKA_CMD & KAFKA_PID=$!; exec bash\"" &
    echo "Kafka server started with PID: $KAFKA_PID"
}

cleanup() {
    echo -e "\nStopping servers..."
    if [ -n "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID"
        echo "Frontend server (PID $FRONTEND_PID) stopped."
    fi
    if [ -n "$MESSAGES_PID" ]; then
        kill "$MESSAGES_PID"
        echo "Messages microservice (PID $MESSAGES_PID) stopped."
    fi
        if [ -n "$KARAFKA_PID" ]; then
        kill "$KARAFKA_PID"
        echo "Karafka message server (PID $KARAFKA_PID) stopped."
    fi
    if [ -n "$KAFKA_PID" ]; then
        kill "$KAFKA_PID"
        echo "Main Kafka cluster (PID $KAFKA_PID) stopped."
    fi
    if [ -n "$BACKEND_PID" ]; then
        kill "$BACKEND_PID"
        echo "Backend server (PID $BACKEND_PID) stopped."
    fi
 
    exit 0
}

# --- Main Script ---
# Trap Ctrl+C (SIGINT) to gracefully stop servers
trap cleanup SIGINT

# Start servers
start_frontend
start_messages
start_karafka
start_backend
start_kafka

echo "Development servers started. Press Ctrl+C to stop."

# Keep the script running until interrupted
wait
