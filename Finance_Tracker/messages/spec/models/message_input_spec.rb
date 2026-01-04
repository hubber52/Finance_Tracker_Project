require 'rails_helper'

RSpec.describe MessageInput, type: :model do
  describe "validations" do
    it "is valid with valid attributes" do
      message_input = MessageInput.new(
        uuid: SecureRandom.uuid,
        message: "This is a valid message",
        sent: "True",
        email: "test@example.com"
      )

      expect(message_input).to be_valid
    end

    it "is not valid without a uuid" do
      message_input = MessageInput.new(
        message: "This message has no uuid"
      )

      expect(message_input).not_to be_valid
      expect(message_input.errors[:uuid]).to include("can't be blank")
    end

    it "is not valid without a message" do
      message_input = MessageInput.new(
        uuid: SecureRandom.uuid
      )

      expect(message_input).not_to be_valid
      expect(message_input.errors[:message]).to include("can't be blank")
    end
  end

  describe "Full object creation" do
    it "Successfully add object to MessageInput model" do
      message_input = MessageInput.new(message: "T",
                                        uuid: SecureRandom.uuid,
                                        phone: "+12345678901",
                                        sent: "True",
                                        email: "test@example.com")

      expect(message_input).to be_valid
    end

    it "Unuccessfully add object to MessageInput model" do
      message_input = MessageInput.new(message: "T",
                                        uuid: SecureRandom.uuid,
                                        phone: 12345678901,
                                        sent: "True",
                                        email: "test@example.com")

      expect(message_input).to be_valid
    end
  end
end
