class AddEmailToMessageInputs < ActiveRecord::Migration[8.1]
  def change
    add_column :message_inputs, :email, :string
  end
end
