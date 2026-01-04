class AddPhoneToUser < ActiveRecord::Migration[8.1]
  def change
    add_column :users, :phone, :integer
  end
end
