<template>
  <view class="pwd-retrieve-container">
		<view class="header">
			<u--text
				v-if="!isResetPassword"
				text="第一次进入系统，必须先重置密码。"
				:size="33"
				align="center"
			>
			</u--text>
		</view>
    <uni-forms ref="form" :value="form" labelWidth="80px">
      <uni-forms-item name="newPassword" label="新密码">
        <uni-easyinput type="password" v-model="form.password" placeholder="请输入新密码" />
      </uni-forms-item>
      <uni-forms-item name="confirmPassword" label="确认密码">
        <uni-easyinput type="password" v-model="form.password_two" placeholder="请确认新密码" />
      </uni-forms-item>
			<u-button text="提交" @click="submit" type="primary"></u-button>
    </uni-forms>
  </view>
</template>

<script>
	import { postCurrentUserResetPassword } from '@/common/request/api/vadmin/auth/user.js'
	
  export default {
    data() {
      return {
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
		computed: {
			isResetPassword() {
				return this.$store.state.auth.isResetPassword
			}
		},
    onReady() {
      this.$refs.form.setRules(this.rules)
    },
    methods: {
      submit() {
        this.$refs.form.validate().then(res => {
					this.$modal.loading("正在提交")
          postCurrentUserResetPassword(this.form).then(response => {
						this.form = {
							password: "",
							password_two: ""
						}
            this.$modal.msgSuccess("重置成功")
						if (!this.isResetPassword) {
							this.$store.commit('auth/SET_IS_RESET_PASSWORD', true)
							this.$tab.reLaunch('/pages/index')
						}
          }).finally(() => {
						this.$modal.closeLoading()
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
		
		.header {
			padding-bottom: 36rpx;
		}
  }
</style>
