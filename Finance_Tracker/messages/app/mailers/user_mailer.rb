#require_relative "../../config/external_secret_key"

class UserMailer < ApplicationMailer
  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.user_mailer.notification_mailer.subject
  #
  default from: Rails.application.credentials.dig(:GOOGLE, :GOOGLE_EMAIL)
  def notification_mailer(email, message)
    @message = message
    @email = email
    mail(to: @email, subject: 'Debt Status', from: Rails.application.credentials.dig(:GOOGLE, :GOOGLE_EMAIL))
  end
end
