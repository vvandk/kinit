<template>
  <view class="pwd-retrieve-container">
    <uni-forms ref="form" :value="form" labelWidth="80px">
      <uni-forms-item name="newPassword" label="新密码">
        <uni-easyinput type="password" v-model="form.password" placeholder="请输入新密码" />
      </uni-forms-item>
      <uni-forms-item name="confirmPassword" label="确认密码">
        <uni-easyinput type="password" v-model="form.password_two" placeholder="请确认新密码" />
      </uni-forms-item>
      <button :loading="btnLoading" type="primary" @click="submit">提交</button>
    </uni-forms>
  </view>
</template>

<script>
	import { postCurrentUserResetPassword } from '@/common/request/api/vadmin/auth/user.js'
	
  export default {
    data() {
      return {
				btnLoading: false,
        form: {
          password: undefined,
          password_two: undefined
        },
        rules: {
          password: {
            rules: [{
                required: true,
                errorMessage: '新密码不能为空',
              },
              {
                minLength: 8,
                maxLength: 20,
                errorMessage: '长度在 8 到 20 个字符'
              }
            ]
          },
          password_two: {
            rules: [{
                required: true,
                errorMessage: '确认密码不能为空'
              }, {
                validateFunction: (rule, value, data) => data.password === value,
                errorMessage: '两次输入的密码不一致'
              }
            ]
          }
        }
      }
    },
    onReady() {
      this.$refs.form.setRules(this.rules)
    },
    methods: {
      submit() {
        this.$refs.form.validate().then(res => {
					this.btnLoading = true
          postCurrentUserResetPassword(this.form).then(response => {
            this.$modal.msgSuccess("修改成功")
          }).finally(() => {
						this.btnLoading = false
					})
        })
      }
    }
  }
</script>

<style lang="scss">
  page {
    background-color: #ffffff;
  }

  .pwd-retrieve-container {
    padding-top: 36rpx;
    padding: 15px;
  }
</style>
