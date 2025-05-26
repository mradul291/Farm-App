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
      <p class="text-center text-gray-600 mt-4">
        Already have an account?
        <a class="text-green-500" href="/login">Log in</a>
      </p>
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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div class="mb-4">
              <label class="block text-gray-700">Account type *</label>
              <div class="flex items-center mt-1">
                <input
                  class="mr-2"
                  id="processor-yes"
                  name="processor"
                  type="radio"
                  value="Individual"
                  v-model="form.account_type"
                  @change="toggleProcessorFields"
                />
                <label class="mr-4" for="processor-yes">Individual</label>
                <input
                  class="mr-2"
                  id="processor-no"
                  name="processor"
                  type="radio"
                  value="Company"
                  v-model="form.account_type"
                  @change="toggleProcessorFields"
                />
                <label for="processor-no">Company</label>
              </div>
              <p v-if="errors.account_type" class="text-red-500 text-sm mt-1">
                {{ errors.account_type }}
              </p>
            </div>
          </div>

          <div class="mb-4" v-if="form.account_type === 'Company'">
            <div class="mb-4">
              <label class="block text-gray-700" for="crop-field"
                >Company name *</label
              >
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.company_name,
                  'border-gray-300': !errors.company_name,
                }"
                id="last-name"
                placeholder="Company Name"
                type="text"
                v-model="form.company_name"
              />

              <p v-if="errors.company_name" class="text-red-500 text-sm mt-1">
                {{ errors.company_name }}
              </p>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700" for="address"
              >Residential address *</label
            >
            <input
              class="w-full border p-2 rounded mt-1"
              :class="{
                'border-red-500': errors.address,
                'border-gray-300': !errors.address,
              }"
              id="address"
              placeholder="Residential address"
              type="text"
              v-model="form.address"
            />
            <p v-if="errors.address" class="text-red-500 text-sm mt-1">
              {{ errors.address }}
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div class="mb-4">
              <label class="block text-gray-700" for="id-type">ID Type</label>
              <select
                class="w-full border border-gray-300 p-2 rounded mt-1"
                id="id-type"
                v-model="form.idType"
              >
                <option value="">Select...</option>
                <option value="Driver's License">Driver's License</option>
                <option value="National Identity Number">
                  National Identity Number
                </option>
                <option value="International Passport">
                  International Passport
                </option>
                <option value="Permanent Voter's Card">
                  Permanent Voter's Card
                </option>
              </select>
            </div>
            <div class="mb-4">
              <label class="block text-gray-700" for="id-number"
                >ID number</label
              >
              <input
                class="w-full border p-2 rounded mt-1"
                :class="{
                  'border-red-500': errors.idNumber,
                  'border-gray-300': !errors.idNumber,
                }"
                id="id-number"
                placeholder="Enter your selected ID number"
                type="text"
                v-model="form.idNumber"
              />
              <p v-if="errors.idNumber" class="text-red-500 text-sm mt-1">
                {{ errors.idNumber }}
              </p>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700" for="id-document"
              >Upload ID document</label
            >
            <input
              class="w-full border border-gray-300 p-2 rounded mt-1"
              id="id-document"
              type="file"
              @change="handleFileUpload($event, 'ID')"
            />
            <p v-if="errors.idDocument" class="text-red-500 text-sm mt-1">
              {{ errors.idDocument }}
            </p>
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
        account_type: '',
        company_name: '',
        address: '',
        idType: '',
        idNumber: '',
        idDocument: null,
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

    'form.address'(value) {
      this.errors.address = value ? '' : 'Address is required'
      if (value) {
        delete this.errors.address
      }
    },

    'form.account_type'(value) {
      this.errors.account_type = value ? '' : 'Account type is required'
      if (value) {
        delete this.errors.account_type
      }
    },
    'form.company_name'(value) {
      if (value && this.form.account_type === 'Company') {
        this.errors.company_name = value ? '' : 'Company name is required'
      } else {
        this.errors.account_type = ''
        delete this.errors.account_type
      }
    },
    'form.idNumber'(value) {
      if (this.form.idType && !value) {
        this.errors.idNumber = "Selected ID's Number is required"
      } else {
        this.errors.idNumber = ''
        delete this.errors.idNumber
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
          user_type: 'vendor',
          first_name: this.form.firstName,
          last_name: this.form.lastName,
          email: this.form.email,
          phone: `${this.form.phoneCode}${this.form.phone}`, // Combining country code and phone
          gender: this.form.gender,
          location: this.form.address, // Mapping address field
          new_password: this.form.password, // Using password field
          id_type: this.form.idType, // id_Type, id_number are not yet stored in DB as fields are not fixed yet in forms
          id_number: this.form.idNumber, //
          account_type: this.form.account_type,
          company_name: this.form.company_name,
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
          console.log('User Registration Success:', data)
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

        formData.append('user_type', 'vendor')

        formData.append('user_email', this.response.user_id)
        formData.append('farmer_id', this.response.farmer_id)

        formData.append('supplier_id', this.response.supplier_id) 

        formData.append('profile_image', this.form.profilePicture)
        formData.append('id_document', this.form.idDocument)

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

        if (!this.form.address) {
          this.errors.address = 'Address is required'
        }

        if (!this.form.account_type) {
          this.errors.account_type = 'Account type is required'
        }

        // Additional validations only if processor is "Yes"
        if (this.form.account_type === 'Company') {
          if (!this.form.company_name) {
            this.errors.company_name = 'Company name is required'
          }
        }

        // Validate ID number only if ID type is selected
        if (this.form.idType && !this.form.idNumber) {
          this.errors.idNumber = "Selected ID's Number is required"
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
    handleFileUpload(event, flag) {
      const file = event.target.files[0]
      if (file) {
        if (file.type !== 'application/pdf') {
          alert('Only PDF files are allowed!')
          return
        }
        if (file.size > 10 * 1024 * 1024) {
          alert('File size must be less than 10MB!')
          return
        }
        if (flag == 'ID') {
          this.form.idDocument = file
          console.log('ID')
        }

        // let formData = new FormData()
        // formData.append('file', file, file.name)
        // this.upload_file(formData)
      }
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
              this.response.farm_id = respo.data.farm_id
              this.response.farmer_id = respo.data.farmer_id

              const is_uploaded = await this.upload_file()

              if (is_uploaded) {
                console.log('Redirecting to login...')
                this.toast.success('Registration successful!')
                window.location.href = '/login' // Redirect to Frappe login page
              } else {
                this.toast.error('Registration failed: Due to File Upload')
                console.error('Registration failed: Due to File Upload')
              }
            } else {
              this.toast.error(`Registration failed: ${respo.message}`)
              console.error('Registration failed:', respo.message)
            }
          } catch (error) {
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
  name: 'farmerRegister',
}
</script>
