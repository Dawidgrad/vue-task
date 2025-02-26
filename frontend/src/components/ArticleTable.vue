<template>
  <q-table :rows="articles" :columns="columns" row-key="id">
    <template v-slot:body-cell-content="props">
      <q-td :props="props" :style="props.col.name === 'content' ? 'max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;' : ''">
        {{ props.value }}
      </q-td>
    </template>
    <template v-slot:body-cell-actions="props">
      <q-td :props="props" class="text-right">
        <q-btn flat icon="edit" @click="$emit('edit', props.row)" />
        <q-btn flat icon="delete" color="red" @click="$emit('delete', props.row.id)" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface Article {
  id?: number;
  title: string;
  content: string;
  release_date: string;
}

const props = defineProps<{ articles: Article[] }>();
const emit = defineEmits<{
  (e: 'edit', article: Article): void;
  (e: 'delete', id: number): void;
}>();

const columns = [
  { name: 'id', label: 'ID', field: 'id' },
  { name: 'title', label: 'Title', field: 'title' },
  { name: 'content', label: 'Content', field: 'content' },
  { name: 'release_date', label: 'Release Date', field: 'release_date' },
  { name: 'actions', label: 'Actions', field: 'actions' },
];
</script>
