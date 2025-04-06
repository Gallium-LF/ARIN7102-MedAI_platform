<template>
  <div class="about">
    <!-- 左侧 Logo -->
    <div class="logo-section">
      <div class="logo-container">
        <img src="@/assets/logo_noback.png" alt="MedAI Logo" class="logo" />
        <a-button type="primary" class="home-button" @click="goToHome"
          >Try it now!</a-button
        >
      </div>
    </div>

    <!-- 中间单词 -->
    <div class="text-section">
      <div class="word-line delay-1">YOUR</div>
      <div class="word-line delay-2">SMART</div>
      <div class="word-line delay-3">PHARMA</div>
      <div class="word-line delay-4">SALES</div>
      <div class="word-line delay-5">ASSISTANT</div>
    </div>

    <!-- 右侧 MedAI -->
    <div class="medai-section">
      <div class="medai-container delay-0">
        <div class="medai-rotated">MEDAI</div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    const router = useRouter();

    const goToHome = () => {
      router.push({ name: "aiagent" }); // Ensure route name matches your router configuration
    };

    return {
      goToHome,
    };
  },
});
</script>

<style scoped>
.about {
  display: flex;
  height: 100vh;
  background: linear-gradient(
    135deg,
    #e1f4f8,
    #f5afff
  ); /* Gradient background */
  font-family: "Segoe UI", sans-serif;
  overflow: hidden;
}

/* 左侧 logo */
.logo-section {
  flex: 0 0 20%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Logo container */
.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* Initially set logo opacity to 0 */
.logo {
  width: 320px;
  height: auto;
  opacity: 0; /* Set initial opacity to 0 */
  animation: fadeInLogo 1.5s ease-out forwards; /* Add fade-in animation for logo */
}

/* Button styles */
.home-button {
  width: 200px;
  height: 45px;
  font-size: 18px;
}

/* 中间文字区域 */
.text-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  padding-right: 100px;
  gap: 0px;
}

.word-line {
  font-size: 125px;
  font-weight: 700;
  color: #203040;
  opacity: 0;
  transform: translateX(100px);
  animation: fadeInFromRight 0.8s ease-out forwards;
}

/* 右侧 MedAI */
.medai-section {
  width: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.medai-container {
  height: 100%;
  display: flex;
  align-items: center;
  transform: rotate(90deg);
  transform-origin: center;
  opacity: 0;
  transform: rotate(90deg) translateX(100px); /* Initial offset position */
  animation: fadeInMedAI 1s ease-out forwards;
}

/* 内容文字 */
.medai-rotated {
  font-size: 180px;
  font-weight: 900;
  color: #0b3c5d;
  white-space: nowrap;
  line-height: 1;
}

/* 动画 */
@keyframes fadeInFromRight {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInMedAI {
  to {
    opacity: 1;
    transform: rotate(90deg) translateX(0);
  }
}

@keyframes fadeInLogo {
  to {
    opacity: 1;
  }
}

/* 延迟控制：每个都有独立动画 */
.delay-0 {
  animation-delay: 0.3s;
}
.delay-1 {
  animation-delay: 1s;
}
.delay-2 {
  animation-delay: 1.3s;
}
.delay-3 {
  animation-delay: 1.6s;
}
.delay-4 {
  animation-delay: 1.9s;
}
.delay-5 {
  animation-delay: 2.2s;
}

/* 应用动画 */
.delay-0 {
  animation-name: fadeInMedAI;
}
.delay-1 {
  animation-name: fadeInFromRight;
}
.delay-2 {
  animation-name: fadeInFromRight;
}
.delay-3 {
  animation-name: fadeInFromRight;
}
.delay-4 {
  animation-name: fadeInFromRight;
}
.delay-5 {
  animation-name: fadeInFromRight;
}
</style>
