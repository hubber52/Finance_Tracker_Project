class Api::UserController < ApplicationController
    
  before_action :set_user, only: [:show, :update, :destroy]

  #User Get all users
  def index
    @users = User.all
    render json: @users, status: :ok
  end

  #Get a specific user
  def show
    render json: @user, status: :ok
  end

  #Page to create a new user
  def new
    render json: {}, status: :ok
  end

  #Create a new user
  def create
    @user = User.new(user_params)
    if @user.save
      render json: @user, status: :created
    else
      render json: { errors: @user.errors.full_messages }, 
                  status: :unprocessable_entity
        
    end
  end

  #Edit the user
  def update
    unless @user.update(user_params)
      render json: { errors: @user.errors.full_messages }, 
                  status: :unprocessable_entity
    end
  end

  #Delete a user
  def destroy
    @user.destroy
    render json: {}, status: :ok
  end

  private
   def user_params
    params.permit(:username, 
                  :password,
                  :phone, 
                  :email, 
                  :uuid)
  end

  def set_user
    @user = User.find(params[:id])
  end
end
