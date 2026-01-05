class MessageInputsConsumer < ApplicationConsumer
  #require_relative "../../config/external_secret_key"

  #Kafka consumer from "Ruby_Message_Service topic"
  #Consume method reads from topic and saves to Postgres DB
  def consume
    messages.each do |loop_message|
      
      begin
        debt_data = JSON.parse(loop_message.raw_payload)
      rescue JSON::ParserError => e
        Rails.logger.error("Failed to parse message payload: #{e.message} - Payload: #{loop_message.raw_payload}")
        next
      end

      if debt_data[4] == Rails.application.credentials.SECRET_KEY
        uuid = debt_data[0]
        message = debt_data[1]
        phone = debt_data[2]
        email = debt_data[3]
        @debt_message = MessageInput.new(message: message, 
                                        uuid: uuid, 
                                        phone: phone,
                                        sent: "False",
                                        email: email)

        if @debt_message.save
          Rails.logger.info("Debt status updated")
        else
          Rails.logger.error("Failed to update debt status: #{@debt_message.errors.full_messages}")
        end
      else
        Rails.logger.error("Invalid Post Data: #{debt_data.inspect}")
      end

    end
  end
end
        
