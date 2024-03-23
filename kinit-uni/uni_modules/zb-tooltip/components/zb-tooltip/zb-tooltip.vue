<template>
	<view class="zb-tooltip" :style="{
		'--theme-bg-color':color
	}">
		<view  class="zb_tooltip_content" @click.stop="handleClick">
			<slot></slot>
			<view class="zb_tooltip__popper"
        @click.stop="()=>{}"
        :style="[style,{
				visibility:isShow?'visible':'hidden',
				color:color==='white'?'':'#fff',
				boxShadow: color==='white'?'0 3px 6px -4px #0000001f, 0 6px 16px #00000014, 0 9px 28px 8px #0000000d':''
			}]" >
				<slot name="content">{{content}}</slot>
				<view class="zb_popper__icon"  :style="[arrowStyle]" :class="[{
					'zb_popper__up':placement.indexOf('bottom')===0,
					'zb_popper__arrow':placement.indexOf('top')===0,
					'zb_popper__right':placement.indexOf('right')===0,
					'zb_popper__left':placement.indexOf('left')===0,
				}]">
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	export default {
		props:{
			visible:Boolean,
			color:{
				type:String,
				default:'#303133',
			},
			placement:{
				type:String,
				default:'top',
			},
			content:{
				type:String,
				default:''
			},
			show:{
				type:Boolean,
				default:false,
			}
		},

		data() {
			return {
				isShow :this.visible,
				title: 'Hello',
				arrowLeft:0,
				query:null,
				style:{

				},
				arrowStyle:{}
			}
		},
		onLoad() {

		},
		watch:{
			isShow:{
				handler(val){
					this.$emit('update:visible', val)
				},
				immediate:true,
			},
			visible:{
				 handler(val){
					 if(val){
						 this.$nextTick(()=>{
							 this.getPosition()
						 })
					 }
           this.isShow = val
				 },
				 immediate:true,
			}
		},
		mounted(){
			// #ifdef H5
			window.addEventListener('click',()=>{
				this.isShow = false
			})
			// #endif
      this.getPosition()
		},
		methods: {
			close(){
				this.isShow = false
			},
			fixedWrap(){
				this.isShow = false
			},
      async handleClick(){
			  if(this.isShow){
          return this.isShow = false
        }
        await this.getPosition()
        this.isShow = true
      },
			getPosition(){
			  return new Promise((resolve) => {
          uni.createSelectorQuery().in(this).selectAll('.zb_tooltip_content,.zb_tooltip__popper').boundingClientRect(async (data)=>{
            let {left,bottom,right,top,width,height} = data[0]
            let obj1 = data[1]
            let objStyle = {}
            let objStyle1 = {}
            switch(this.placement){
              case 'top':
                if(obj1.width > width){
                  objStyle.left = `-${(obj1.width - width)/2}px`
                }else{
                  objStyle.left = `${Math.abs(obj1.width - width)/2}px`
                }

                objStyle.bottom =`${height+8}px`
                objStyle1.left = (obj1.width/2-6)+'px'
                break;
              case 'top-start':
                objStyle.left = `0px`
                objStyle.bottom =`${height+8}px`
                break;
              case 'top-end':
                objStyle.right = `0px`
                objStyle.bottom =`${height+8}px`
                objStyle1.right=`8px`
                break;
              case 'bottom':
                if(obj1.width>width){
                  objStyle.left = `-${(obj1.width - width)/2}px`
                }else{
                  objStyle.left = `${Math.abs(obj1.width - width)/2}px`
                }
                objStyle.top =`${height+8}px`
                objStyle1.left = (obj1.width/2-6)+'px'
                break;
              case 'bottom-start':
                objStyle.left = `0px`
                objStyle.top =`${height+8}px`
                objStyle1.left = `8px`
                break;

              case 'bottom-end':
                objStyle.right = `0px`
                objStyle.top =`${height+8}px`
                objStyle1.right = `8px`
                break;

              case 'right':
                objStyle.left = `${width+8}px`
                if(obj1.height>height){
                  objStyle.top =`-${(obj1.height - height)/2}px`
                }else{
                  objStyle.top =`${Math.abs((obj1.height - height)/2)}px`
                }

                objStyle1.top = `${obj1.height/2-6}px`
                break;
              case 'right-start':
                objStyle.left = `${width+8}px`
                objStyle.top =`0px`
                objStyle1.top = `8px`
                break;

              case 'right-end':
                objStyle.left = `${width+8}px`
                objStyle.bottom =`0px`
                objStyle1.bottom = `8px`
                break;

              case 'left':
                objStyle.right = `${width+8}px`

                if(obj1.height>height){
                  objStyle.top =`-${(obj1.height - height)/2}px`
                }else{
                  objStyle.top =`${Math.abs((obj1.height - height)/2)}px`
                }

                objStyle1.top = `${obj1.height/2-6}px`
                break;

              case 'left-start':
                objStyle.right = `${width+8}px`
                objStyle.top =`0px`
                objStyle1.top = `8px`
                break;

              case 'left-end':
                objStyle.right = `${width+8}px`
                objStyle.bottom =`0px`
                objStyle1.bottom = `8px`
                break;
            }
            this.style = objStyle
            // 三角形箭头
            this.arrowStyle = objStyle1
            resolve()
          }).exec()
        })

			}
		}
	}
</script>

<style lang="scss" scoped>
	$theme-bg-color: var(--theme-bg-color);

	.zb-tooltip{
		position: relative;

	}
	.zb_tooltip_content{
		height: 100%;
		/* float: left; */
		position: relative;
		display: inline-block;

		// display: flex;
		// flex-direction: row;
		// align-items: center;
		/* overflow: hidden; */
	}
	.zb_tooltip__popper{
		/* transform-origin: center top; */
		background: $theme-bg-color;

		visibility: hidden;
		// color:'#fff';
		position: absolute;
		    border-radius: 4px;
			font-size: 12px;
			padding: 10px;
			min-width: 10px;
			word-wrap: break-word;
			display: inline-block;
			white-space: nowrap;
			z-index:9;
	}
	.zb_popper__icon{
		width: 0;
		height: 0;
		z-index:9;
		position: absolute;
	}
	.zb_popper__arrow{
		bottom: -5px;
		/* transform-origin: center top; */
		border-left: 6px solid transparent;
		    border-right: 6px solid transparent;
		    border-top: 6px solid $theme-bg-color;

	}
	.zb_popper__right{
		border-top: 6px solid transparent;
		    border-bottom: 6px solid transparent;
		    border-right: 6px solid $theme-bg-color;
			left:-5px;
	}

	.zb_popper__left{
		border-top: 6px solid transparent;
		border-bottom: 6px solid transparent;
		border-left: 6px solid $theme-bg-color;
		right:-5px;
	}

	.zb_popper__up{
		border-left: 6px solid transparent;
		    border-right: 6px solid transparent;
		    border-bottom: 6px solid $theme-bg-color;
			top:-5px;
	}
	.fixed{
		position: absolute;width: 100vw;
		height:  100vh;
		position: fixed;
		left: 0;
		top: 0;
	pointer-events: auto;
		background: red;
		z-index:-1;
	}
</style>
