class CreateMessageInputs < ActiveRecord::Migration[8.1]
  def change
    create_table :message_inputs do |t|
      t.string :uuid
      t.string :message

      t.timestamps
    end
  end
end
