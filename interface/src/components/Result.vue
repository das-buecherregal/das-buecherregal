<template>
  <div class="result">
    <div class="top">
      <div class="left">
        <div class="title">{{meta.title}}</div>
        <div class="author">Author: {{meta.author}} {{dateString}}</div>
        <div class="sizes">
          <div class="type" v-if="!isSect">Entire Text ({{meta.section_count}} Chapters)</div>
          <div
            class="type"
            v-bind:class="{sect: isSect}"
            v-else
          >Chunk {{parseInt(sectNumb) + 1}}/{{meta.section_count}}</div>
          <div
            class="stats"
          >{{Number(sentenceCount).toLocaleString()}} Sentences &#8729; {{Number(wordCount).toLocaleString()}} Words &#8729; {{Number(charCount).toLocaleString()}} Characters</div>
        </div>
      </div>
      <div class="links">
        <a
          class="link epub"
          download=""
          v-bind:href="this.epubUrl"
        >
          <span>
            <strong>Download EPUB</strong>
          </span>
          <img src="./../assets/download.png" alt />
        </a>
        <a
          class="link"
          target="_blank"
          v-bind:href="'https://www.gutenberg.org/ebooks/' + this.id.split('.')[0]"
        >
          <span>
            Text via
            <strong>Project Gutenberg</strong>
          </span>
          <img src="./../assets/open_out_b.png" alt />
        </a>
        <a
          v-if="this.wikipedia != ''"
          class="link wikipedia"
          target="_blank"
          v-bind:href="this.wikipedia"
        >
          <span>
            Author's
            <strong>Wikipedia ({{wiki_lang}})</strong>
          </span>
          <img src="./../assets/open_out_b.png" alt />
        </a>
      </div>
    </div>
    <div class="total" v-if="rules.length > 0">
      {{Number(rank).toLocaleString()}} match<span v-if="rank != 1">es</span> on selected rule<span v-if="rules.length != 1">s</span>
    </div>
    <div class="rule_matches" v-if="rules.length > 0">
      <RuleSummary
        v-for="(rule, index) in rules"
        v-show="!ruleLimit || (target[rule] >= ruleLimitNumb)"
        :key="index"
        :count="target[rule]"
        :title="rules_json[rule]['title']"
        :matches="ruleMatches[rule]"
        :leftovers="matchLeftover[rule]"
      />
    </div>
  </div>
</template>

<script>
var pako = require("pako");
import rules_json_imp from "../assets/ruleDefs.json";
import wikipedia_json from "../assets/wikipedia.json";
const RuleSummary = () => import("./RuleSummary.vue");
export default {
  name: "Result",
  components: {
    RuleSummary
  },
  computed: {
    epubUrl() {
      if (this.isSect) {
        var mid = this.id;
        mid = mid.split(".")[0];
        return `${this.BASE_URL}/chunk_epubs/${mid}.${this.sectNumb + 1}.epub`;
      }
      return `https://www.gutenberg.org/ebooks/${this.id}.epub.images`;
    },
    dateString() {
      if (this.meta.birthdate == undefined && this.meta.deathdate == undefined) {
        return "";
      }
      else if (this.meta.birthdate != undefined && this.meta.deathdate != undefined) {
        return `(${this.meta.birthdate}-${this.meta.deathdate})`;
      }
      else if (this.meta.birthdate != undefined) {
        return `(Born ${this.meta.birthdate}, Death Unknown)`;
      }
      else {
        return `(Died ${this.meta.deathdate}, Birth Year Unknown)`;
      }
    },
  },
  watch: {
    rules: function() {
      this.updateResult();
    }
  },
  props: {
    id: String,
    isSect: Boolean,
    meta: Object,
    sectNumb: Number,
    rules: Array,
    rank: Number,
    charCount: Number,
    wordCount: Number,
    sentenceCount: Number,
    target: Array,
    ruleLimit: Boolean,
    ruleLimitNumb: Number
  },
  data: function() {
    return {
      rules_json: rules_json_imp,
      wikipedia: "",
      wiki_lang: "",
      BASE_URL: process.env.VUE_APP_BASE_URL,
      ruleJson: {},
      matchLeftover: {},
      ruleMatches: {}
    };
  },
  created() {
    var wiki_target = wikipedia_json[this.id.split(".")[0]];
        if (wiki_target != null) {
          if (wiki_target["de"] != null) {
            this.wikipedia = wiki_target["de"];
            this.wiki_lang = "DE";
          } else {
            this.wikipedia = wiki_target["en"];
            this.wiki_lang = "EN";
          }
        }
  },
  mounted() {
    this.updateResult();
  },
  methods: {
    updateResult() {
       this.getRuleJson().then(() => {
      var sub = "whole";
      if (this.isSect) {
        var temp = this.id.split(".");
        sub = temp[1];
      }
      var ruleMatches = {};
      this.rules.forEach(r => {
        ruleMatches[r] = [];
        if (!this.isSect) {
          Object.values(this.ruleJson).map(j => {
            ruleMatches[r] = ruleMatches[r]
              .concat(j[3][r])
              .splice(0, 7);
          });
        } else {
          ruleMatches[r] = this.ruleJson[sub][3][r];
        }
      });

      this.ruleMatches = ruleMatches;
    }).then(() => {
      var l = {}
      this.rules.forEach(r => {
        l[r] = this.target[r] - this.ruleMatches[r].length
      });
      this.matchLeftover = l;
    });
    },
    getRuleJson() {
      var mid = this.id;
      if (this.isSect) {
        mid = mid.split(".")[0];
      }
      return (fetch(`${this.BASE_URL}/rules/${mid}.txt`).then(raw => {
        return raw.text();
      }).then(text => {
        var decoded = atob(text);
        this.ruleJson = JSON.parse(pako.inflate(decoded, { to: "string" }));
      }));
    }
  }
};
</script>

<style>
.rule_matches {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  margin-top: 5px;
  border-top: 2px solid #ccc;
}

.sizes {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 5px;
}

.sizes .stats {
  margin-top: 0;
  padding-top: 0;
  font-size: 0.8rem;
  color: #aaa;
}

.result {
  box-sizing: border-box;
  width: 95%;
  max-width: 1000px;
  padding: 10px;
  background-color: white;
  margin: 8px;
  border: 1px solid #ddd;
  border-radius: 2px;
  box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.04);
}

.author {
  font-size: 0.9rem;
  margin-bottom: 3px;
}

.type {
  display: inline-block;
  font-size: 0.7em;
  margin-right: 8px;
  padding: 3px;
  background-color: #fbf1ff;
  color: #6800917a;
  font-weight: 900;
  text-transform: uppercase;
  text-align: center;
}

.type.sect {
  background-color: #fff7f1;
  color: #915e007a;
}

.result .title {
  font-size: 1.2rem;
  font-style: italic;
  font-weight: 600;
  margin-bottom: 3px;
}

.total {
  font-size: 0.8rem;
  font-style: italic;
  margin-top: 10px;
}

.links {
  right: 0px;
  /* padding-right: 5px; */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  flex-shrink: 0;
  justify-content: flex-start;
}

.link {
  display: inline-block;
  font-size: 0.73rem;
  cursor: pointer;
  font-weight: normal;
  padding: 6px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid #cfcaaf;
  color: black;
  background-color: #eceadf;
  box-shadow: 0 0 4px 2px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-bottom: 7px;
  text-decoration: none;
}

.link:last-of-type {
  margin-bottom: 0;
}

.link.wikipedia {
  background-color: whitesmoke;
  border-color: #bbb;
}

.link.epub {
  background-color: rgb(255, 235, 219);
}

.link img {
  margin-left: 8px;
  height: 1.1rem;
}

.top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
}

.left {
  padding-right: 20px;
}

@media only screen and (max-width: 1000px) {
  
  .top {
    flex-direction: column;
  }
  .links {
    flex-direction: row-reverse;
    width: 100%;
    align-items: flex-end;
    justify-content: center;
    flex-wrap: wrap;
  }
  .link {
    margin-right: 10px;
    margin-bottom: 5px;
    margin-top: 5px;
  }
  .link:first-of-type {
    margin-right: 0;
  }
  .link:last-of-type {
  margin-bottom: auto;
}

}
  @media only screen and (max-width: 700px) {
    .left.title, .left.author {
      text-align: center;
    }
    .author {
      margin-bottom: 14px;
    }
    .sizes {
      text-align: center;
      justify-content: center;
    }
    .type {
      margin-bottom: 4px;
    }
    .stats {
      margin-bottom: 14px;
    }
    .links {
      margin-top: 5px;
    }
    .link {
      font-size: 0.9rem;
      padding: 10px;
      width: 100%;
      margin-top: 5px;
      margin-right: 0;
    }
    .link.wikipedia {
      width: 100%;
    }
    
    details {
      margin-right: 0px;
      width: 100%;
    }

    .match_texts {
      margin-left: 3px;
      margin-right: 0px;
    }
  }
</style>
