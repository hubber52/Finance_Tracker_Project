require 'spec_helper'
require_relative '../../app/consumers/application_consumer'
require_relative '../../app/consumers/message_inputs_consumer'


RSpec.describe MessageInputsConsumer, type: :consumer do
  # Include the Karafka testing helpers
  include Karafka::Testing::Helpers

  #Define test data
  let(:valid_payload) do
    [
      SecureRandom.uuid,
      "True",
      "+12345678901",
      "test@example.com",
      Rails.application.credentials.SECRET_KEY
    ].to_json
  end

  let(:invalid_payload) do
    [
      SecureRandom.uuid,
      "True",
      "+12345678901",
      "test@example.com",
      "Random Secret"
    ].to_json
  end

  #Define metadata for karafka consumer
  subject(:consumer) { karafka.consumer_for('Ruby_Message_Service') }

  describe '#consume' do
    before do
      # Simulate sending the messages to Kafka
      karafka.produce(valid_payload)
      karafka.produce(invalid_payload)
      allow(Karafka.logger).to receive(:info)
    end

    it 'Processes the incoming message correctly' do
      expect {
        # Here you simulate consuming the message with the right helpers
        consumer.consume
      }.to change(MessageInput, :count).by(1)  # Expecting that the message will create a new MessageInput
    end

    it "Rejects incoming message due to invalid secret" do
      expect{
        consumer.consume
    }.to change(MessageInput, :count).by(1) #Expect that message will not create a new MessageInput object
    end
  end
end
