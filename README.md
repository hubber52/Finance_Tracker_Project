Finance tracker project by Tommy Liang.

To run backend:
Navigate to env/bin
"source activate"
Navigate to Finance_Tracker
"python manage.py runserver"

To run frontend:
Navigate to Finance_Tracker/frontend
"npm run dev"
Frontend runs on localhost:5173

To run primary Kafka cluster:
Navigate to Finance_Tracker/kafka

KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties

"bin/kafka-server-start.sh config/server.properties"


To run message microservice
Navigate to Finance_Tracker/messages
"rails server"
Microservice runs on localhost:3000

to run message microservice kafka instance:
Navigate to Finance_Tracker/messages
"bundle exec karafka server"

To run Ngrok gateway for message microservice:
"ngrok http 3000"

