class AddColumnToMessageInputs < ActiveRecord::Migration[8.1]
  def change
    add_column :message_inputs, :phone, :string
    add_column :message_inputs, :sent, :string
  end
end
