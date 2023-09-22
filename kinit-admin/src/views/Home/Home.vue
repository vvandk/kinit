<script setup lang="ts">
import { ElCard, ElRow, ElCol, ElTabs, ElTabPane, ElAvatar } from 'element-plus'
import { computed, ref } from 'vue'
import InfoWrite from './components/InfoWrite.vue'
import PasswordWrite from './components/PasswordWrite.vue'
import { useAuthStoreWithOut } from '@/store/modules/auth'
import avatar from '@/assets/imgs/avatar.jpg'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'

const activeName = ref('info')

const authStore = useAuthStoreWithOut()

let genderOptions = ref<DictDetail[]>([])

const getOptions = async () => {
  const dictStore = useDictStore()
  const dictOptions = await dictStore.getDictObj(['sys_vadmin_gender'])
  genderOptions.value = dictOptions.sys_vadmin_gender
}

getOptions()

const user = computed(() => authStore.getUser)
</script>

<template>
  <div class="p-20px">
    <ElRow :gutter="20">
      <ElCol :xs="24" :sm="12" :md="8">
        <ElCard shadow="hover" class="pb-30px">
          <div class="text-center">
            <ElAvatar :size="80" :src="user.avatar ? user.avatar : avatar" />
            <p style="font-size: 24px">{{ user.name }}</p>
          </div>
          <div class="pl-20px pt-30px">
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">姓名:</span>
              <span class="pl-10px">{{ user.name }}</span>
            </div>
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">昵称:</span>
              <span class="pl-10px">{{ user.nickname }}</span>
            </div>
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">手机号:</span>
              <span class="pl-10px">{{ user.telephone }}</span>
            </div>
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">性别:</span>
              <span class="pl-10px">{{
                selectDictLabel(genderOptions, user.gender as string)
              }}</span>
            </div>
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">角色:</span>
              <span class="pl-10px">{{ user.roles?.map((item) => item.name).join(',') }}</span>
            </div>
            <div class="leading-relaxed">
              <span class="pl-10px w-80px inline-block">创建时间:</span>
              <span class="pl-10px">{{ user.create_datetime }}</span>
            </div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="16">
        <ElCard shadow="hover">
          <ElTabs v-model="activeName">
            <ElTabPane label="基本信息" name="info">
              <InfoWrite />
            </ElTabPane>
            <ElTabPane label="修改密码" name="password">
              <PasswordWrite />
            </ElTabPane>
          </ElTabs>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>
