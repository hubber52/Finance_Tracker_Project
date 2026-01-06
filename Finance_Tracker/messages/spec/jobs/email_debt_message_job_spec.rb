require 'rails_helper'

RSpec.describe EmailDebtMessageJob, type: :job do
  let(:message_params) { { email: 'test@example.com', message: 'You have a negative balance' } }
  
  # Mock the mailer to avoid sending emails during the test
  before do
    allow(UserMailer).to receive_message_chain(:notification_mailer, :deliver_now).and_return(true)
  end

  describe "#perform" do
    it "sends an email for unsent messages" do
      #Create an unsent message
      message_input = MessageInput.new(
        uuid: SecureRandom.uuid,
        message: "t",
        sent: "False",
        email: "test@example.com"
      )
      message_input.save
      # Enqueue the job
      EmailDebtMessageJob.perform_now

      #Get message item from database
      message_input.reload

      # Expect the job update the "sent" flag
      expect(message_input).to be_valid
      expect(message_input.sent).to eq("True")
    end
    
    it "skips sent messages" do
      #Create an sent message
      message_input = MessageInput.new(
        uuid: SecureRandom.uuid,
        message: "t",
        sent: "True",
        email: "test@example.com"
      )
      message_input.save
      # Enqueue the job
      EmailDebtMessageJob.perform_now

      #Get message item from database
      message_input.reload

      # Expect the job to not process the message
      expect(message_input).to be_valid
      expect(message_input.sent).to eq("True")
    end
  end
end
