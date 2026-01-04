class ChangeUserUuidColumn < ActiveRecord::Migration[8.1]
  def change
    enable_extension 'pgcrypto'
    remove_column :users, :uuid, :string
  end
end
