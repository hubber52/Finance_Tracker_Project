class ApplicationMailer < ActionMailer::Base
  default from: Rails.application.credentials.DEFAULT_EMAIL
  layout "mailer"
end
