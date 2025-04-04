<template>
  <!-- Loader Overlay -->
  <div
    v-if="loading"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-40"
  >
    <div
      class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-16 w-16"
    ></div>
  </div>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <a class="text-green-600" @click="$emit('goBack')" href="#">
        <i class="fas fa-arrow-left"></i> Back home
      </a>
      <a class="text-gray-600" href="#">
        Already have an account?
        <span class="text-green-600">Log in</span>
      </a>
    </div>
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h2 class="text-2xl font-semibold text-center mb-4">Create Account</h2>
      <form class="multiform" @submit.prevent="handleSubmit">
        <div v-if="step === 1">
          <p class="text-center text-gray-600 mb-8">Personal Information</p>
          <div class="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-gray-700" for="first-name"
                >First Name *</label
              >
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.firstName,
                  'border-gray-300': !errors.firstName,
                }"
                id="first-name"
                placeholder="First Name"
                type="text"
                v-model="form.firstName"
                required
              />
              <p v-if="errors.firstName" class="text-red-500 text-sm mt-1">
                {{ errors.firstName }}
              </p>
            </div>
            <div>
              <label class="block text-gray-700" for="last-name"
                >Last Name *</label
              >
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.lastName,
                  'border-gray-300': !errors.lastName,
                }"
                id="last-name"
                placeholder="Last Name"
                type="text"
                v-model="form.lastName"
              />
              <p v-if="errors.lastName" class="text-red-500 text-sm mt-1">
                {{ errors.lastName }}
              </p>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-gray-700" for="email">Email</label>
            <input
              class="w-full border p-2 rounded mt-1"
              :class="{
                'border-red-500': errors.email,
                'border-gray-300': !errors.email,
              }"
              id="email"
              placeholder="Email"
              type="email"
              v-model="form.email"
              required
            />
            <p v-if="errors.email" class="text-red-500 text-sm mt-1">
              {{ errors.email }}
            </p>
          </div>

          <div class="mb-4">
            <label class="block text-gray-700" for="phone">Phone *</label>
            <div class="flex">
              <select
                class="border p-2 rounded-l"
                :class="{
                  'border-red-500': errors.phone,
                  'border-gray-300': !errors.phone,
                }"
                v-model="form.phoneCode"
              >
                <option value="+234">+234</option>
              </select>
              <input
                class="w-full border p-2 rounded-r"
                :class="{
                  'border-red-500': errors.phone,
                  'border-gray-300': !errors.phone,
                }"
                id="phone"
                placeholder="Phone Number"
                type="text"
                v-model="form.phone"
                required
              />
            </div>
            <p v-if="errors.phone" class="text-red-500 text-sm mt-1">
              {{ errors.phone }}
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-gray-700" for="age-group">Age *</label>
              <input
                type="number"
                id="age-group"
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.age,
                  'border-gray-300': !errors.age,
                }"
                placeholder="Enter Age"
                min="1"
                v-model="form.age"
                required
              />
              <p v-if="errors.age" class="text-red-500 text-sm mt-1">
                {{ errors.age }}
              </p>
            </div>
            <div>
              <label class="block text-gray-700">Gender *</label>
              <div class="flex items-center mt-1">
                <input
                  class="mr-2"
                  id="male"
                  name="gender"
                  type="radio"
                  value="Male"
                  v-model="form.gender"
                />
                <label class="mr-4" for="male">Male</label>
                <input
                  class="mr-2"
                  id="female"
                  name="gender"
                  type="radio"
                  value="Female"
                  v-model="form.gender"
                />
                <label for="female">Female</label>
              </div>
              <p v-if="errors.gender" class="text-red-500 text-sm mt-1">
                {{ errors.gender }}
              </p>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-gray-700" for="profile-picture">
              Upload profile picture (optional)
            </label>
            <div class="flex items-center mt-1">
              <img
                id="profilePic"
                alt="Profile picture"
                class="w-10 h-10 rounded-full mr-4"
                :src="this.profilePictureUrl"
              />
              <input
                type="file"
                id="fileInput"
                @change="changeProfilePicture"
              />
              <!-- <button class="bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    Change Picture
                  </button> -->
            </div>
          </div>

          <div class="flex justify-between">
            <!-- <button class="bg-gray-200 text-gray-700 px-4 py-2 rounded">
                  Back
                </button> -->
            <button
              class="bg-green-600 text-white px-4 py-2 rounded ml-auto"
              @click="nextStep"
            >
              Continue
            </button>
          </div>
        </div>
        <div v-if="step === 2">
          <h2 class="text-2xl font-semibold text-center mb-4">
            Security Setup
          </h2>
          <div class="mb-4">
            <label class="block text-gray-700" for="password">Password *</label>
            <div class="relative">
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.password,
                  'border-gray-300': !errors.password,
                }"
                id="password"
                placeholder="••••••••••••"
                type="password"
                v-model="form.password"
              />
              <button
                class="absolute right-2 top-2 text-gray-600"
                type="button"
                @click="togglePasswordVisibility('password')"
              >
                <i class="fas fa-eye"></i>
              </button>
            </div>
            <p v-if="errors.password" class="text-red-500 text-sm mt-1">
              {{ errors.password }}
            </p>
          </div>

          <div class="mb-4">
            <label class="block text-gray-700" for="confirm-password"
              >Confirm password *</label
            >
            <div class="relative">
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.confirmPassword,
                  'border-gray-300': !errors.confirmPassword,
                }"
                id="confirm-password"
                placeholder="••••••••••••"
                type="password"
                v-model="form.confirmPassword"
              />
              <button
                class="absolute right-2 top-2 text-gray-600"
                type="button"
                @click="togglePasswordVisibility('confirm-password')"
              >
                <i class="fas fa-eye"></i>
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="text-red-500 text-sm mt-1">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <div class="mb-4">
            <h3 class="text-gray-700 font-semibold">Password Requirements</h3>
            <ul class="list-disc list-inside text-gray-600">
              <li>Must be at least 8 characters</li>
              <li>Must contain one special character and one number</li>
              <li>Must contain one uppercase and lowercase letter</li>
            </ul>
          </div>
          <div class="flex justify-between">
            <button
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded"
              @click="previousStep"
            >
              Back
            </button>
            <button
              class="bg-green-600 text-white px-4 py-2 rounded"
              @click="submitForm"
            >
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
const baseUrl = import.meta.env.VITE_BASE_URL
import { useToast } from 'vue-toastification'
// import { useToast } from 'vue-toastification'

export default {
  setup() {
    const toast = useToast()

    return {
      toast,
    }
  },
  data() {
    return {
      step: 1,
      form: {
        firstName: '',
        lastName: '',
        email: '',
        phoneCode: '+234',
        phone: '',
        age: '',
        gender: '',
        profilePicture: null,
        password: '',
        confirmPassword: '',
        // First crop fields (always visible)
      },
      profilePictureUrl:
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrsaTeFqurvUDvMYOcgZAd-JPf-dtLogrrog&s', // Placeholder profile image
      showPassword: false,
      showConfirmPassword: false,
      errors: {},
      response: {
        user_id: '',
      },
      loading: false,
    }
  },
  watch: {
    'form.firstName'(value) {
      const nameRegex = /^[A-Za-z\s]+$/
      if (!value) {
        this.errors.firstName = 'First name is required'
      } else if (!nameRegex.test(value)) {
        this.errors.firstName = 'First name cannot contain numbers'
      } else {
        this.errors.firstName = ''
        delete this.errors.firstName
      }
    },

    'form.lastName'(value) {
      const nameRegex = /^[A-Za-z\s]+$/
      if (!value) {
        this.errors.lastName = 'Last name is required'
      } else if (!nameRegex.test(value)) {
        this.errors.lastName = 'Last name cannot contain numbers'
      } else {
        this.errors.lastName = ''
        delete this.errors.lastName
      }
    },

    'form.email'(value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value) {
        this.errors.email = 'Email is required'
      } else if (!emailRegex.test(value)) {
        this.errors.email = 'Enter a valid email address'
      } else {
        this.errors.email = ''
        delete this.errors.email
      }
    },

    'form.phone'(value) {
      const phoneRegex = /^[0-9]{7,15}$/
      if (!value) {
        this.errors.phone = 'Phone number is required'
      } else if (!phoneRegex.test(value)) {
        this.errors.phone = 'Enter a valid phone number (numbers only)'
      } else {
        this.errors.phone = ''
        delete this.errors.phone
      }
    },
    'form.age'(value) {
      if (!value) {
        this.errors.age = 'Valid age is required'
      } else if (!/^\d+$/.test(value)) {
        this.errors.age = 'Enter a valid age (positive numbers only)'
      } else {
        this.errors.age = ''
        delete this.errors.age
      }
    },

    'form.gender'(value) {
      this.errors.gender = value ? '' : 'Gender is required'
      if (value) {
        delete this.errors.gender
      }
    },

    'form.password'(value) {
      const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

      if (!value) {
        this.errors.password = 'Password is required'
      } else if (!passwordRegex.test(value)) {
        this.errors.password =
          'Password must be at least 8 characters long, contain one uppercase, one lowercase, one number, and one special character'
      } else {
        this.errors.password = ''
        delete this.errors.password
      }
    },

    'form.confirmPassword'(value) {
      if (!value) {
        this.errors.confirmPassword = 'Confirm Password is required'
      } else if (value !== this.form.password) {
        this.errors.confirmPassword = 'Passwords do not match'
      } else {
        this.errors.confirmPassword = ''
        delete this.errors.confirmPassword
      }
    },
  },
  methods: {
    async registerUser() {
      try {
        // Prepare the data object
        const requestData = {
          user_type: 'buyer',
          first_name: this.form.firstName,
          last_name: this.form.lastName,
          email: this.form.email,
          phone: `${this.form.phoneCode}${this.form.phone}`, // Combining country code and phone
          gender: this.form.gender,
          new_password: this.form.password, // Using password field
        }

        console.log({ requestData })
        // API Call
        const response = await fetch(
          `${baseUrl}/api/method/farmer.api.user_api.create_user`,
          {
            method: 'POST', // Fixed "PPOST" typo
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData), // Corrected to pass JSON
          },
        )

        const data = (await response.json()).message

        if (data.status == 201 && data.message) {
          console.log('User Registration Success:', data.message)
          return data
        } else {
          console.error('Unexpected API response format:', data)
          return data
        }
      } catch (err) {
        console.error('Failed to register user:', err)
        return err
      }
    },
    async upload_file() {
      try {
        const formData = new FormData()

        // Append necessary fields to formData
        formData.append('user_type', 'buyer')

        formData.append('user_email', this.response.user_id)
        formData.append('profile_image', this.form.profilePicture)

        const response = await fetch(
          `${baseUrl}/api/method/farmer.api.user_api.upload_profile_picture`,
          {
            method: 'POST', // Use POST for file uploads
            body: formData, // Send formData directly
          },
        )

        const data = (await response.json()).message

        if (data && data.status == 200) {
          console.log('Upload successful:', data.message)
          return true
        } else {
          console.error('Unexpected response format:', data)
          return false
        }
      } catch (err) {
        console.error('Upload failed:', err)
      }
    },
    validateStep() {
      this.errors = {} // Reset errors before validation

      if (this.step === 1) {
        this.errors = {} // Reset previous errors

        const nameRegex = /^[A-Za-z\s]+$/ // Only letters and spaces
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // Basic email format
        const phoneRegex = /^[0-9]{7,15}$/ // Numbers only, min 7 max 15 digits
        const positiveNumberRegex = /^[1-9]\d*$/ // Only positive numbers

        if (!this.form.firstName) {
          this.errors.firstName = 'First name is required'
        } else if (!nameRegex.test(this.form.firstName)) {
          this.errors.firstName = 'First name cannot contain numbers'
        }

        if (!this.form.lastName) {
          this.errors.lastName = 'Last name is required'
        } else if (!nameRegex.test(this.form.lastName)) {
          this.errors.lastName = 'Last name cannot contain numbers'
        }

        if (!this.form.email) {
          this.errors.email = 'Email is required'
        } else if (!emailRegex.test(this.form.email)) {
          this.errors.email = 'Enter a valid email address'
        }

        if (!this.form.phone) {
          this.errors.phone = 'Phone number is required'
        } else if (!phoneRegex.test(this.form.phone)) {
          this.errors.phone = 'Enter a valid phone number (numbers only)'
        }

        if (!this.form.age) {
          this.errors.age = 'Valid age is required'
        } else if (!positiveNumberRegex.test(this.form.age)) {
          this.errors.phone = 'Enter a valid age (positive numbers only)'
        }

        if (!this.form.gender) {
          this.errors.gender = 'Gender is required'
        }
      }

      if (this.step === 2) {
        const passwordRegex =
          /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

        if (!this.form.password) {
          this.errors.password = 'Password is required'
        } else if (!passwordRegex.test(this.form.password)) {
          this.errors.password =
            'Password must be at least 8 characters long, contain one uppercase, one lowercase, one number, and one special character'
        }

        if (!this.form.confirmPassword) {
          this.errors.confirmPassword = 'Confirm Password is required'
        } else if (this.form.confirmPassword !== this.form.password) {
          this.errors.confirmPassword = 'Passwords do not match'
        }
      }
      return Object.keys(this.errors).length === 0 // Return true if no errors
    },
    nextStep() {
      // if (this.step <= 3) this.step++
      console.log('checking error', this.errors)
      if (!this.validateStep()) {
        return // Stop execution if validation fails
      } else if (this.step < 2) {
        this.step++
      }
    },
    previousStep() {
      if (this.step > 1) {
        this.step--
      }
    },
    togglePasswordVisibility(field) {
      if (field === 'password') {
        this.showPassword = !this.showPassword
        document.getElementById('password').type = this.showPassword
          ? 'text'
          : 'password'
      } else if (field === 'confirm-password') {
        this.showConfirmPassword = !this.showConfirmPassword
        document.getElementById('confirm-password').type = this
          .showConfirmPassword
          ? 'text'
          : 'password'
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click() // Triggers hidden input when clicked
    },
    changeProfilePicture(event) {
      const file = event.target.files[0]
      this.form.profilePicture = file

      const reader = new FileReader()
      reader.onload = (e) => {
        this.profilePictureUrl = e.target.result
      }
      reader.readAsDataURL(file)
      // this.profilePictureUrl = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrsaTeFqurvUDvMYOcgZAd-JPf-dtLogrrog&s' // Change to uploaded image

      // handleFileUpload()
    },
    async handleSubmit() {
      if (this.validateStep()) {
        if (this.step === 2) {
          this.loading = true
          try {
            const respo = await this.registerUser() // Call registerUser and get response
            console.log({ respo })

            if (respo && respo.message === 'User Created Successfully') {
              this.response.user_id = respo.data.user_id

              const is_uploaded = await this.upload_file()

              if (is_uploaded) {
                console.log('Redirecting to login...')
                this.toast.success('Registration successful!')
                window.location.href = '/' // Redirect to Frappe login page
              } else {
                console.error('Registration failed: Due to File Upload')
                this.toast.error('Registration failed: Due to File Upload')
              }
            } else {
              console.error('Registration failed:', respo.message)

              this.toast.error(`Registration failed: ${respo.message}`)
            }
          } catch (error) {
            console.error('Failed to register. Please try again!', error)
            this.toast.error(
              `Failed to register. Please try again! :  ${error}`,
            )
          } finally {
            this.loading = false
          }
        }
      } else {
        console.log('Form validation failed:', this.errors, this.validateStep())
      }
    },
  },
  name: 'buyerRegister',
}
</script>
