<template>
  <v-app dark>
    <v-main>
      <v-btn @click="onClicked">
      </v-btn>

      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class DefaultLayout extends Vue {
};
</script>
