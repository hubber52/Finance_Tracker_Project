class UserRegistrationConsumer < ApplicationConsumer
  require_relative '../../config/external_secret_key'
  def consume
    messages.each do |message|
      registration_data = JSON.parse(message.raw_payload)
      if registration_data[3] == DjangoSecretKey::SECRET_KEY
        @user = User.new(username: registration_data[0],
                        email:  registration_data[1],
                        uuid:  registration_data[2])
        puts "User params Received"
        if @user.save
          puts "User created"
        end
      else
        puts "Invalid Post Data: #{registration_data.inspect}"
      end
    end
  end
end