<template>
  <div class="welcome">
    <el-container style="height: 100%;">
      <el-header>
        <div
          style="display: flex;align-items: center;margin-top: 25px;margin-left: 30px;gap: 10px;">
          <img src="@/assets/xiaozhi-logo.png" alt="" style="width: 56px;height: 56px;" />
          <img src="@/assets/xiaozhi-ai.png" alt="" style="width: 78px;height: 16px;" />
        </div>
      </el-header> 
      <el-main style="position: relative;">
        <div style="margin-left: 18%;position: absolute;top: 50%;transform: translateY(-50%);">
          <div style="display: flex;align-items: center;margin-bottom: 27px;">
            <div class="left-pillar" />
            <div class="hi-text-bg" />
            <div class="hi-text">Hi，小智</div>
          </div>
          <div class="introduction">让我们一起探索</div>
          <div class="introduction">人工智能与机器人技术</div>
          <div class="introduction">的迷人世界！</div>
          <div class="hint"
            style="text-align: left;font-weight: 400;font-size: 12px;text-align: left;color: #818cae;">
            Let's explore the fascinating world
          </div>
          <div style="margin-top: 107px;display: flex;gap: 20px;">
            <div class="btn">
              <img src="@/assets/welcome/questions.png" alt="" class="btn-icon" />
              DIY教程
            </div>
            <div class="btn">
              <img src="@/assets/welcome/github.png" alt="" class="btn-icon" />
              GitHub
            </div>
            <div class="btn" style="background: #5778ff;color: #fff;" @click="jumpHome">
              <img src="@/assets/welcome/more.png" alt="" class="btn-icon" />
              控制台
            </div>
          </div>
        </div>
      </el-main>
      <el-footer>
        <div style="font-size: 12px;font-weight: 400;color: #3D4566">
          ©2025 xiaozhi-esp32-server</div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  methods:{
    jumpHome(){
      this.$router.push('/home')
    }
  }
}
</script>
<style scoped lang="scss">
.welcome {
  min-width: 1200px;
  min-height: 675px;
  height: 100vh;
  background-image: url("@/assets/welcome/background.png");
  background-size: cover;
  /* 确保背景图像覆盖整个元素 */
  background-position: center;
  /* 从顶部中心对齐 */
  -webkit-background-size: cover;
  /* 兼容老版本WebKit浏览器 */
  -o-background-size: cover;
  /* 兼容老版本Opera浏览器 */
}
.left-pillar {
  width: 4px;
  height: 36px;
  background: #5778ff;
}
.hi-text-bg {
  width: 129px;
  height: 36px;
  background: linear-gradient(90.66deg, #5778ff 0%, #f5f6fa00 100%);
  opacity: 0.5;
}
.hi-text {
  line-height: 36px;
  font-weight: 700;
  font-size: 18px;
  text-align: left;
  color: #3d4566;
  padding-left: 14px;
  position: absolute;
}
.introduction {
  font-weight: 700;
  font-size: 54px;
  text-align: left;
  color: #3d4566;
}
.btn {
  width: 140px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 28px;
  display: flex;
  gap: 10px;
  font-weight: 400;
  font-size: 16px;
  text-align: left;
  color: #3d4566;
  cursor: pointer;
  background-color: #fff;
}
.btn-icon {
  width: 16px;
  height: 16px;
}
</style>
