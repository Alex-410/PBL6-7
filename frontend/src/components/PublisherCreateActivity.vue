<template>
<div>
<div class="section-title mb-24">发布新活动</div>
<div class="card"><div class="card-body">
<form @submit.prevent="submit">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">活动标题 *</label>
<input class="form-input" v-model="form.title" placeholder="输入活动标题" required/>
</div>
<div class="form-group mb-16">
<label class="form-label">活动类别 *</label>
<select class="form-input" v-model="form.category" required>
<option value="">请选择</option>
<option v-for="c in categories" :key="c" :value="c">{{c}}</option>
</select>
</div>
</div>
<div class="form-group mb-16">
<label class="form-label">活动描述 *</label>
<textarea class="form-input" v-model="form.description" rows="4" placeholder="详细描述活动内容" required></textarea>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">活动主办方 *</label>
<input class="form-input" v-model="form.organizer" placeholder="例：计算机学院" required/>
</div>
<div class="form-group mb-16">
<label class="form-label">最大人数</label>
<input class="form-input" type="number" v-model.number="form.maxCount" min="1" placeholder="100"/>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">开始时间</label>
<input class="form-input" type="datetime-local" v-model="form.startTime"/>
</div>
<div class="form-group mb-16">
<label class="form-label">结束时间</label>
<input class="form-input" type="datetime-local" v-model="form.endTime"/>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">活动地点</label>
<input class="form-input" v-model="form.location" placeholder="例：图书馆报告厅"/>
</div>
<div class="form-group mb-16">
<label class="form-label">标签（逗号分隔）</label>
<input class="form-input" v-model="form.tags" placeholder="AI,讲座,技术"/>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">是否含加分</label>
<select class="form-input" v-model="form.hasBonus" style="max-width:200px">
<option :value="false">否</option>
<option :value="true">是</option>
</select>
</div>
<div v-if="form.hasBonus" class="form-group mb-16">
<label class="form-label">加分类型 *</label>
<select class="form-input" v-model="form.bonusType" required>
<option value="">请选择</option>
<option v-for="t in bonusTypes" :key="t" :value="t">{{t}}</option>
</select>
</div>
</div>
<div v-if="form.hasBonus" class="form-group mb-16">
<label class="form-label">加分分值 *</label>
<input class="form-input" type="number" v-model.number="form.bonusValue" min="0" step="0.5" placeholder="0.5" style="max-width:200px" required/>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="form-group mb-16">
<label class="form-label">报名身份限制</label>
<select class="form-input" v-model="form.registrationLimitType">
<option value="none">任何人均可报名</option>
<option value="college">限制指定学院报名</option>
<option value="club">限制指定社团报名</option>
</select>
</div>
<div v-if="form.registrationLimitType==='college'" class="form-group mb-16">
<label class="form-label">指定学院 *</label>
<select class="form-input" v-model="form.registrationLimitValue" required>
<option value="">请选择学院</option>
<option v-for="c in colleges" :key="c" :value="c">{{c}}</option>
</select>
</div>
<div v-else-if="form.registrationLimitType==='club'" class="form-group mb-16">
<label class="form-label">指定社团 *</label>
<input class="form-input" v-model="form.registrationLimitValue" placeholder="输入社团名称" required/>
</div>
</div>
<div style="display:flex;gap:12px">
<button class="btn" type="submit" :disabled="submitting">{{submitting?'提交中...':'提交审核'}}</button>
<button class="btn btn-secondary" type="button" @click="reset">重置</button>
</div>
<div v-if="msg" style="margin-top:16px;padding:12px;border-radius:var(--radius);font-size:.85rem" :style="{background:ok?'#ecfdf5':'#fef2f2',color:ok?'#065f46':'#991b1b'}">{{msg}}</div>
</form>
</div></div>
</div>
</template>
<script setup lang="ts">
import {ref,reactive} from 'vue'
import {activityApi} from '../services/api'
defineProps<{user:any}>()
defineEmits(['navigate'])
const categories=['学术','文艺','体育','公益','社交','就业','讲座','其他']
const bonusTypes=['综合素质','实践学分','第二课堂','志愿服务','劳动教育','其他']
const colleges=['计算机科学与技术学院','机械工程学院','外国语学院','创业学院','艺术学院','体育部']
const form=reactive({title:'',category:'',description:'',organizer:'',startTime:'',endTime:'',location:'',maxCount:100,tags:'',hasBonus:false,bonusType:'',bonusValue:0,registrationLimitType:'none',registrationLimitValue:''})
const submitting=ref(false)
const msg=ref('')
const ok=ref(false)
async function submit(){
submitting.value=true;msg.value=''
try{
const payload={...form,fee:0,status:'pending'}
const res=await activityApi.create(payload)
if(res.code===200){ok.value=true;msg.value='活动已提交，等待管理员审核！';reset()}
else{ok.value=false;msg.value=res.message||'提交失败'}
}catch(e:any){ok.value=false;msg.value=e?.response?.data?.message||'提交失败，请重试'}
finally{submitting.value=false}
}
function reset(){form.title='';form.category='';form.description='';form.organizer='';form.startTime='';form.endTime='';form.location='';form.maxCount=100;form.tags='';form.hasBonus=false;form.bonusType='';form.bonusValue=0;form.registrationLimitType='none';form.registrationLimitValue=''}
</script>
