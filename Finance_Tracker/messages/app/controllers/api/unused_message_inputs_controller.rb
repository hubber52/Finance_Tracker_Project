class Api::MessageInputsController < ApplicationController

  rescue_from ActiveRecord::RecordNotFound do
    render json: { error: "Message not found" }, status: :not_found
  end

  #skip_before_action :authenticate_request, only: [:create]
  before_action :set_message, only: [:show, :update, :destroy]

  #Get all messages
  def index
    @msgs = MessageInput.all
    render json: @msgs, status: :ok
  end

  #Get a specific message
  def show
    render json: @msg, status: :ok
  end

  #Create a new message
  def create
    @msg = MessageInput.new(message_params)
    if @msg.save
      render json: @msg, status: :created
    else
      Rails.logger.error("Failed to create message: #{@msg.errors.full_messages}")
      render json: { errors: @msg.errors.full_messages }, 
                  status: :unprocessable_entity
    end
  end

  #Edit the message
  def update
    if @msg.update(message_params)
      render json: @msg, status: :ok
    else
      Rails.logger.error("Failed to update message: #{@msg.errors.full_messages}")
      render json: { errors: @msg.errors.full_messages }, status: :unprocessable_entity
    end
  end

  #Delete a message
  def destroy
    if @msg.destroy
      head :no_content  # Sends a 204 status
    else
      Rails.logger.error("Failed to delete message: #{@msg.errors.full_messages}")
      render json: { errors: @msg.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private
    def message_params
      params.require(:message_input).permit(:uuid, :messages)
    end

    def set_message
      @msg = MessageInput.find(params[:id])
    end
end