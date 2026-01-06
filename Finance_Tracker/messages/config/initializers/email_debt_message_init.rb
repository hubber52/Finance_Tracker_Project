if Rails.env.production? || Rails.env.development?
  Rails.application.config.after_initialize do
    EmailDebtMessageJob.perform_later
  end
end