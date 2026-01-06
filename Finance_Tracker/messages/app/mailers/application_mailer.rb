class ApplicationMailer < ActionMailer::Base
  default from: Rails.application.config.email
  layout "mailer"
end
