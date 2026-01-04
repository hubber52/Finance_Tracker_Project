require "test_helper"

class UserTest < ActiveSupport::TestCase

  test "create user" do
    puts "user creation test"
    user = User.create(email:"DOWNCASE@TEST.COM", username: "DOWNCASE", password: "Test")
    assert_equal("DOWNCASE", user.username)
    assert_equal("downcase@test.com", user.email)
    assert_equal("Test", user.password)
  end
  
end
