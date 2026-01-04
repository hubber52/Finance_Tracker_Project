class MessageInput < ApplicationRecord
  validates :message, presence: true
  validates :uuid, presence: true
  validates :sent, presence: true
  validates :email, presence: true
end
