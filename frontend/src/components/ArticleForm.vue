<template>
  <q-dialog v-model="localShow">
    <q-card style="width: 600px; max-width: 90vw;">
      <q-card-section>
        <q-input v-model="articleData.title" label="Title" />
        <q-input v-model="articleData.content" label="Content" type="textarea" />
        <q-input
            v-model="articleData.release_date"
            label="Release Date (YYYY-MM-DD)"
            mask="####-##-##"
            outlined
            dense
            class="q-mb-md"
            :error="dateError"
            :error-message="dateErrorMessage"
            @blur="validateDate"
          />
      </q-card-section>
      <q-card-actions>
        <q-btn label="Save" color="primary" @click="save" />
        <q-btn label="Cancel" color="grey" @click="cancel" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
// sa
<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';

interface Article {
  id?: number;
  title: string;
  content: string;
  release_date: string;
}

const props = defineProps<{
  show: boolean;
  article: Article | null;
}>();

const emit = defineEmits<{
  (e: 'save', article: Article): void;
  (e: 'update:show', value: boolean): void;
}>();

const localShow = ref(props.show);

watch(() => props.show, (newVal) => {
  localShow.value = newVal;
});

watch(localShow, (val) => {
  emit('update:show', val);
});

const articleData = ref<Article>(
  props.article ? { ...props.article } : { title: '', content: '', release_date: '' }
);

watch(() => props.article, (newArticle) => {
  articleData.value = newArticle ? { ...newArticle } : { title: '', content: '', release_date: '' };
});

const validateDate = () => {
  const datePattern = /^\d{4}-\d{2}-\d{2}$/;
  if (!datePattern.test(articleData.value.release_date)) {
    dateError.value = true;
    dateErrorMessage.value = "Invalid format. Use YYYY-MM-DD.";
    return;
  }

  const [year, month, day] = articleData.value.release_date.split("-").map(Number);
  const date = new Date(year, month - 1, day);

  if (
    date.getFullYear() !== year ||
    date.getMonth() + 1 !== month ||
    date.getDate() !== day
  ) {
    dateError.value = true;
    dateErrorMessage.value = "Invalid date. Please enter a real date.";
  } else {
    dateError.value = false;
    dateErrorMessage.value = "";
  }
};

const save = () => {
  emit('save', articleData.value);
  localShow.value = false;
};

const cancel = () => {
  localShow.value = false;
};
</script>
