class EmailDebtMessageJob < ApplicationJob

  queue_as :default

  def perform(*args)
    #Identify unsent messages, and try to send them.
    @unsent_messages = MessageInput.where(sent: "False")
    #Need to add retry count, and drop excessive retries into dead letter queue
    
    @unsent_messages.each do |single_message|
      Rails.logger.info("#{single_message.id} #{single_message.sent} #{single_message.uuid} #{single_message.email}, \n")

      if single_message.message == 't'
        begin
          UserMailer.notification_mailer(email=single_message.email, 
          message="You have a negative balance").deliver_now
        rescue StandardError => e
          Rails.logger.error("Email failed to send: #{e.message}")
        end

      elsif single_message.message == 'f'
        begin
          UserMailer.notification_mailer(email=single_message.email, 
          message="You no longer have a negative balance").deliver_now
        rescue StandardError => e
          Rails.logger.error("Email failed to send: #{e.message}")
        end
      else
        Rails.logger.error("Invalid Input")
      end

      #If successful, update the "sent" flag
      single_message.update(sent: "True")
    end
    
    self.class.set(wait: 5.seconds).perform_later(*args)
  end
end
