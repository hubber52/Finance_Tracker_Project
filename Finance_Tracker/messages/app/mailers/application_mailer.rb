class ApplicationMailer < ActionMailer::Base
  default from: Rails.application.credentials.dig(:GOOGLE, :GOOGLE_EMAIL)
  layout "mailer"
end
