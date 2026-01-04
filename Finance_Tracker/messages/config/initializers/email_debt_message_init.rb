Rails.application.config.after_initialize do
    EmailDebtMessageJob.perform_later
end