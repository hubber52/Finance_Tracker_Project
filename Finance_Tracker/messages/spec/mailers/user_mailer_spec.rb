require "rails_helper"

RSpec.describe UserMailer, type: :mailer do
  before do
    ActionMailer::Base.deliveries.clear
  end

  describe "notification_mailer" do
    let(:email) { "testuser@example.com" }
    let(:message) { "You have a new debt notification." }

    it "sends the notification email" do
      # Deliver the email
      puts "14 #{email}"
      UserMailer.notification_mailer(email, message).deliver_now

      # Ensure one email was sent
      expect(ActionMailer::Base.deliveries.count).to eq(1)

      # Retrieve the last email sent
      sent_email = ActionMailer::Base.deliveries.last

      # Verify the email properties
      expect(sent_email.to).to eq([email])
      expect(sent_email.subject).to eq("Debt Status")
      expect(sent_email.body.encoded).to match(message)
      expect(sent_email.from).to eq(['tommy.liang300@gmail.com'])
    end
  end
end
