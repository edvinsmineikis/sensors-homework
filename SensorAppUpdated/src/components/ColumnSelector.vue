<template>
    <v-container>
        <v-row>
            <v-col cols="4" v-for="(metricsChunk, index) in metricsChunks" :key="index">
                <div v-for="metric in metricsChunk" :key="metric.id">
                    <v-switch v-model="metric.enabled" :label="metric.name" @change="onSwitchChange"></v-switch>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>
  
<script>
export default {
    props: {
        metrics: {
            required: true
        }
    },
    computed: {
        metricsChunks() {
            const chunkSize = 5;
            const chunks = [];
            console.log(this.metrics);
            for (let i = 0; i < this.metrics.length; i += chunkSize) {
                chunks.push(this.metrics.slice(i, i + chunkSize));
            }
            return chunks;
        }
    },
    methods: {
        onSwitchChange() {
            this.$emit("switch-changed");
        }
    }

}
</script>
  
  