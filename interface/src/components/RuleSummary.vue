<template>
  <details>
    <summary class="match_head">
      <div class="summary_flex">
        <div class="match_count">{{count}}</div>
        <div class="rule_title">{{title}}</div>
      </div>
    </summary>
    <div v-if="count > 0" class="match_texts">
      <div class="text_match" v-for="(match, mc) in matches" :key="mc">
        ...{{match[0]}}
        <span class="match_hl">{{match[1]}}</span>
        {{match[2]}}...
      </div>
      <div v-if="leftovers != 0" class="match_more">
        {{Number(leftovers).toLocaleString()}} more match<span v-if="leftovers > 1">es not shown</span>
      </div>
    </div>
    <div class="frown" v-if="count == 0"><span>&#9785;</span>No matches for this rule</div>
  </details>
</template>

<script>
export default {
  name: "RuleSummary",
  props: {
    count: Number,
    title: String,
    matches: Array,
    leftovers: Number
  }
};
</script>

<style>

summary {
    cursor: pointer;
}

.match_head {
  box-sizing: border-box;
}

.match_head * {
  transform: translateY(-1.3px);
}

.match_count {
  display: inline-block;
  font-size: 0.85rem;
  text-align: center;
  color: white;
  min-width: 30px;
  padding: 0 7px 0 7px;
  margin-right: 7px;
  border-radius: 10px;
  font-weight: bolder;
  background-color: #0366d6;
}

.rule_title {
  font-size: 0.9rem;
}

.summary_flex {
  padding: 5px 0 5px 0;
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.match_texts {
  border-left: 3px solid #0366d6;
  margin-left: 30px;
  display: flex;
  flex-direction: column;
}

.text_match {
  padding: 15px;
  border-bottom: 1px dashed #ccc;
  font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
  font-size: 12px;
  color: #444;
  line-height: 130%;
}

.text_match .match_hl {
  background-color: rgba(255, 223, 93, 0.2);
  mix-blend-mode: multiply;
  color: black;
  font-weight: 500;
  border-bottom: 1px solid #ffd33d;
}

.match_texts:last-child {
  border-bottom: 2px solid #ccc;
  margin-bottom: 10px;
}

.frown {
  margin-left: 20px;
  font-size: 0.8rem;
  margin-bottom: 10px;
}

.frown span {
  transform: translateY(4px);
  margin-right: 8px;
  font-size: 1.5rem;
  display: inline-block;
}

.match_more {
  text-align: center;
  padding: 10px;
  font-size: 0.85rem;
  font-style: italic;
  background-color: #f7f9fc;
  color: #000000;
}

.total {
  font-size: 0.8rem;
  font-style: italic;
}
</style>
