class ApplicationMailer < ActionMailer::Base
  default from: Rails.application.credentials.GOOGLE.GOOGLE_EMAIL
  layout "mailer"
end
