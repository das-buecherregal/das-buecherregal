<template>
  <div id="app" v-bind:class="{showresults: showResults}">
    <div class="header">
      <a href="https://www.brown.edu/academics/german-studies/" class="brown">
        <strong>Brown</strong> German Studies
      </a>
      <div class="main_logo">Das Bücherregal</div>
      <div class="info">?</div>
    </div>
    <div class="headerBack">
      <div class="backButton" @click="showResults = false">&larr;</div>
    </div>
    <div class="sidebar">
      <div class="form_group">
        <div class="stick h2stick">
          <div class="h2">Text Length</div>
        </div>
        <div class="inset">
          <div id="rule_checkboxes">
            <div
              class="rule_checkbox inset_item no-bottom"
              v-bind:class="{providing: length_restrict}"
              @click="length_restrict = !length_restrict"
            >
              <div class="check_container">
                <input type="checkbox" v-model="length_restrict" />
              </div>
              <div class="desc">
                <div class="title">Restrict Length</div>
                <div class="bodyt sub">Only show texts with a specified length</div>
              </div>
            </div>
            <div
              class="inset_item rule_checkbox opts full"
              v-bind:class="{available: length_restrict}"
            >
              <select style="width:105px;" v-model="overunder" :disabled="!length_restrict">
                <option disabled value>Please select one</option>
                <option>At least</option>
                <option>Fewer than</option>
              </select>
              <input
                style="width:60px;"
                :disabled="!length_restrict"
                v-model.number="count"
                type="number"
              />
              <select style="width:105px;" v-model="unit" :disabled="!length_restrict">
                <option disabled value>Please select one</option>
                <option>Characters</option>
                <option>Words</option>
                <option>Sentences</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="form_group">
        <div class="stick h2stick">
          <div class="h2">Text Type</div>
          <div
            class="bodyt sub warn"
            v-if="!(whole_texts && partial_texts) && show_warn"
          >You cannot deselect both options.</div>
        </div>
        <div class="inset">
          <div id="rule_checkboxes">
            <div
              class="rule_checkbox inset_item"
              @click="() => {
                    if (partial_texts) {
                      show_warn = false
                      whole_texts = !whole_texts
                    } else {
                      show_warn = true
                    }
                  }"
            >
              <div class="check_container">
                <input
                  type="checkbox"
                  v-bind:disabled="whole_texts && !partial_texts"
                  v-model="whole_texts"
                />
              </div>
              <div class="desc">
                <div class="title">Show Full Texts</div>
                <div class="bodyt sub">Return results for complete Project Gutenberg ebooks</div>
              </div>
            </div>
            <div
              class="rule_checkbox inset_item"
              @click="() => {
                    if (whole_texts) {
                      show_warn = false
                      partial_texts = !partial_texts
                    } else {
                      show_warn = true
                    }
                  }"
            >
              <div class="check_container">
                <input
                  type="checkbox"
                  v-bind:disabled="partial_texts && !whole_texts"
                  v-model="partial_texts"
                />
              </div>
              <div class="desc">
                <div class="title">Show Chunks</div>
                <div class="bodyt sub">Return results for individual EPUB chunks</div>
                <div class="bodyt sub explain">
                  <details
                    @click="() => {
                    if (whole_texts) {
                      show_warn = false
                      partial_texts = !partial_texts
                    } else {
                      show_warn = true
                    }
                  }"
                  >
                    <summary>What is this?</summary>
                    <div
                      class="explainer"
                    >Selecting this feature will include shorter passages of the text in the results.</div>
                  </details>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="form_group">
        <div class="stick h2stick">
          <div class="h2">Author Era</div>
        </div>
        <div class="inset">
          <div id="rule_checkboxes">
            <div
              class="rule_checkbox inset_item no-bottom"
              v-bind:class="{providing: date_restrict}"
              @click="date_restrict = !date_restrict"
            >
              <div class="check_container">
                <input type="checkbox" v-model="date_restrict" />
              </div>
              <div class="desc">
                <div class="title">Restrict Dates</div>
                <div class="bodyt sub">Only show texts written by authors of a certain date range</div>
              </div>
            </div>
            <div id="rule_checkboxes">
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Before 1848'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Before 1848" />
                </div>
                <div class="desc">Alive before 1848</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Before 1888'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Before 1888" />
                </div>
                <div class="desc">Alive before 1888</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Between 1870 1914'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Between 1870 1914" />
                </div>
                <div class="desc">Alive between 1870 and 1914</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Between 1890 1919'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Between 1890 1919" />
                </div>
                <div class="desc">Alive between 1890 and 1919</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Between 1914 1933'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Between 1914 1933" />
                </div>
                <div class="desc">Alive between 1914 and 1933</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single"
                @click="dateRange = 'Alive Between 1933 1945'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Alive Between 1933 1945" />
                </div>
                <div class="desc">Alive between 1933 and 1945</div>
              </div>
              <div
                class="inset_item rule_checkbox opts single nobottom"
                @click="dateRange = 'Custom'"
                v-bind:class="{available: date_restrict}"
              >
                <div class="check_container">
                  <input type="radio" v-model="dateRange" value="Custom" />
                </div>
                <div class="desc">Custom</div>
              </div>
              <div
                class="inset_item rule_checkbox opts full"
                v-bind:class="{available: dateRange == 'Custom' && date_restrict}"
              >
                <select style="width:70px;" v-model="timeoverunder" :disabled="!date_restrict">
                  <option disabled value>Please select one</option>
                  <option>Born</option>
                  <option>Died</option>
                  <option>Alive</option>
                </select>
                <select style="width:90px;" v-model="timerange" :disabled="!date_restrict">
                  <option disabled value>Please select one</option>
                  <option>Before</option>
                  <option>After</option>
                  <option>Between</option>
                </select>
                <div style="display:flex; flex-direction: row; align-items: center;">
                  <input style="width:35px;" :disabled="!date_restrict" v-model.number="year" />
                  <div v-if="timerange == 'Between'">and</div>
                  <input
                    v-if="timerange == 'Between'"
                    style="width:35px;"
                    :disabled="!date_restrict"
                    v-model.number="range_end"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="form_group">
        <div class="stick h2stick ruleHead">
          <div class="h2">Rules</div>
          <div class="bodyt">Find texts with matching grammars</div>
          <div class="header_check">
            <input type="checkbox" id="rule_limit_check" v-model="ruleLimit" />
            <label for="rule_limit_check">
              Only include rules with more than
              <input
                v-model.number="ruleLimitNumb"
                type="number"
                id="ruleLimitNumbInput"
              /> matches
            </label>
          </div>
        </div>
        <div class="inset">
          <div id="rule_checkboxes">
            <div v-for="(group, gi) in ruleGroupDefs" :key="gi">
              <div class="ruleSubheader">{{gi}}</div>
              <div
                class="rule_checkbox inset_item"
                v-for="rule in ruleGroupDefs[gi]"
                :key="rule['i']"
                v-bind:class="{ active: ruleIsActive(`${rule['i']}`) }"
                @click="toggleRule(`${rule['i']}`)"
              >
                <div class="check_container">
                  <input type="checkbox" :id="rule['i']" :value="rule['i']" v-model="checkedRules" />
                </div>
                <div class="desc">
                  <div class="title">{{rule.title}}</div>
                  <div class="bodyt sub">{{rule.description}}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="results">
      <Result
        v-for="t in this.filtered"
        :key="t.id"
        :id="t['id']"
        :target="t['target']"
        :isSect="t.isSect"
        :rank="t.rank"
        :sectNumb="parseInt(t.sectNumber)"
        :charCount="t.lCnt"
        :wordCount="t.wCnt"
        :sentenceCount="t.sCnt"
        v-bind:meta="getMeta(t)"
        :rules="checkedRules"
        :ruleLimit="ruleLimit"
        :ruleLimitNumb="ruleLimitNumb"
      />
      <div class="noResults" v-if="allFiltered.length == 0">Sorry, no results found</div>
      <div id="pagecontrol">
        <div class="pagination" v-show="allFiltered.length > 0">
          <div class="pageback" v-bind:class="{vis: this.page > 0}" @click="pagedown()">&larr;</div>
          Page {{this.page + 1}} of {{Number(this.totalPages).toLocaleString()}}
          <div
            class="pageforward"
            v-bind:class="{vis: this.page + 1 < this.totalPages}"
            @click="pageup()"
          >&rarr;</div>
        </div>
        <div class="resCount" v-show="allFiltered.length > 0">
          {{Number(allFiltered.length).toLocaleString()}} Result<span v-if="allFiltered.length > 1">s</span>
        </div>
      </div>
    </div>
    <div id="goresults" @click="showResults = true">
      <div class="gobutton">See Results &rarr;</div>
    </div>
  </div>
</template>

<script>
import ruleGroupDefsJson from "./assets/ruleGroupDefs.json";
import rule_counts_json from "./assets/rule_counts.json";
const texts_json = () => import("./assets/texts_meta.json");
const Result = () => import("./components/Result.vue");

export default {
  name: "GDS-App",
  components: {
    Result
  },
  data: function() {
    return {
      ruleGroupDefs: ruleGroupDefsJson, // Initialize imported JSON for rules
      rule_counts: rule_counts_json, // Initialize imported JSON for rule counts

      showResults: false, // Controller for results view on the small screens

      page: 0, // Page number
      perPage: 20, // Page length

      texts: {}, // Object to hold text info, will be loaded asynchronously from texts_json

      allFiltered: [], // All results tgat match
      filtered: [], // Up to this.per_page results, representing a page of results, filtered from this.allFiltered

      whole_texts: true, // Should whole texts be shown?
      partial_texts: true, // Should partial texts be shown?
      show_warn: false, // Warning for attempt at deselecting both text types

      length_restrict: false, // Should we restrict results based on text length?
      overunder: "At least", // Length Restrict: "Fewer than" or "At least"
      unit: "Words", // Length Restrict: "Words", "Characters", or "Sentences"
      count: 10, // Length Restrict: Numebr of this.unit

      dateRange: "Alive Before 1848", // Selected Date Range
      date_restrict: false, // Should we restrict results based on author dates?
      timerange: "Before", // Dates: look "Before", "Between", or "After"
      timeoverunder: "Born", // Dates: "Born", "Alive", or "Died"
      year: 1800, // Dates: Only relevant date if this.timeoverunder == "Before" or "After", first date in range if "Between"
      range_end: 1900, // Dates: Only relevant as range end date if this.timeoverunder == "Between"

      checkedRules: [], // Array holding indices of selected rules
      ruleLimit: true, // Should we only inlcude rule matches where the number of matches > this.ruleLimitNumb?
      ruleLimitNumb: 5 // Number of matches to use with ruleLimit
    };
  },
  beforeMount() {},
  computed: {
    totalPages() {
      var base = Math.floor(this.allFiltered.length / this.perPage);
      if (this.allFiltered.length % this.perPage != 0) {
        base += 1;
      }
      return base;
    },
    controller() {
      return `${this.whole_texts}|${this.partial_texts}|${this.length_restrict}|${this.overunder}|${this.count}|${this.unit}|${this.checkedRules}|${this.date_restrict}|${this.timerange}|${this.timeoverunder}|${this.year}|${this.range_end}|${this.ruleLimit}|${this.ruleLimitNumb}`;
    }
  },
  mounted() {
    texts_json()
      .then(data => {
        this.texts = data;
      })
      .then(() => {
        this.updateFilter();
      });
  },
  methods: {
    pageup() {
      if (this.page < this.totalPages) {
        this.page += 1;
        this.updatePageResults();
      }
    },
    pagedown() {
      if (this.page > 0) {
        this.page -= 1;
        this.updatePageResults();
      }
    },
    updatePageResults() {
      this.filtered = []
        .concat(this.allFiltered)
        .splice(this.page * this.perPage, this.perPage);
    },
    updateFilter() {
      this.allFiltered = Object.values(this.texts)
        .map(text => {
          return text;
        })
        .filter(text => {
          return (
            (this.whole_texts && !text.isSect) ||
            (this.partial_texts && text.isSect)
          );
        })
        .filter(text => {
          if (!this.length_restrict) {
            return true;
          }
          var op;
          switch (this.unit) {
            case "Characters":
              op = text.lCnt;
              break;
            case "Words":
              op = text.wCnt;
              break;
            case "Sentences":
              op = text.sCnt;
              break;
          }
          var bool = op >= this.count;
          if (this.overunder == "Fewer than") {
            bool = !bool;
          }
          return bool;
        })
        .filter(text => {
          return text.id != undefined;
        })
        .map(text => {
          var rank = 0;
          var mid = text.id;
          var sub = "whole";
          if (text.isSect) {
            mid = text["parent"];
            sub = text["sectNumber"];
          }
          this.checkedRules.forEach(activeRule => {
            if (this.ruleLimit) {
              var add = this.rule_counts[mid][sub][activeRule];
              if (add >= this.ruleLimitNumb) {
                rank += add;
              }
            } else {
              rank += this.rule_counts[mid][sub][activeRule];
            }
          });
          var updated = text;
          updated["rank"] = rank;
          try {
            updated["target"] = this.rule_counts[mid][sub];
          } catch {
            console.log(text, mid, sub);
          }
          return updated;
        })
        .filter(text => {
          if (!this.date_restrict) {
            return true;
          }
          var m = this.getMeta(text);
          var birth = parseInt(m.birthdate);
          var death = parseInt(m.deathdate);
          if (this.timeoverunder == "Born") {
            if (m.birthdate == undefined) {
              return false;
            } else if (this.timerange == "Before") {
              return birth <= this.year;
            } else if (this.timerange == "After") {
              return birth >= this.year;
            } else {
              return birth >= this.year && birth <= this.range_end;
            }
          } else if (this.timeoverunder == "Died") {
            if (m.deathdate == undefined) {
              return false;
            }
            if (this.timerange == "Before") {
              return death <= this.year;
            } else if (this.timerange == "After") {
              return death >= this.year;
            } else {
              return death >= this.year && death <= this.range_end;
            }
          } else {
            if (m.birthdate == undefined || m.deathdate == undefined) {
              return false;
            }
            if (this.timerange == "Before") {
              return birth <= this.year;
            } else if (this.timerange == "After") {
              return death >= this.year;
            } else {
              return (
                (birth <= this.year && death >= this.year) ||
                (birth >= this.year && birth <= this.range_end)
              );
            }
          }
        })
        .filter(a => a.rank != 0 || this.checkedRules.length == 0)
        .sort((a, b) => b.rank - a.rank);

      this.page = 0;
      this.updatePageResults();
    },
    getMeta(i) {
      if (i.isSect) {
        return this.texts[i.parent].metadata;
      }
      return i.metadata;
    },
    ruleIsActive(i) {
      return this.checkedRules.includes(i);
    },
    toggleRule(i) {
      if (this.ruleIsActive(i)) {
        this.checkedRules.splice(
          this.checkedRules.findIndex(v => v === i),
          1
        );
      } else {
        this.checkedRules.push(i);
      }
    }
  },
  watch: {
    controller: function() {
      this.updateFilter();
    },
    dateRange: function() {
      if (this.dateRange == "Alive Before 1848") {
        this.timeoverunder = "Alive";
        this.timerange = "Before";
        this.year = 1848;
        // range_end
      } else if (this.dateRange == "Alive Before 1888") {
        this.timeoverunder = "Alive";
        this.timerange = "Before";
        this.year = 1888;
        // range_end
      } else if (this.dateRange == "Alive Between 1870 1914") {
        this.timeoverunder = "Alive";
        this.timerange = "Between";
        this.year = 1870;
        this.range_end = 1914;
      } else if (this.dateRange == "Alive Between 1890 1919") {
        this.timeoverunder = "Alive";
        this.timerange = "Between";
        this.year = 1890;
        this.range_end = 1919;
      } else if (this.dateRange == "Alive Between 1914 1933") {
        this.timeoverunder = "Alive";
        this.timerange = "Between";
        this.year = 1914;
        this.range_end = 1933;
      } else if (this.dateRange == "Alive Between 1933 1945") {
        this.timeoverunder = "Alive";
        this.timerange = "Between";
        this.year = 1933;
        this.range_end = 1945;
      }

      this.updateFilter();
    }
  }
};
</script>

<style>
html,
body,
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: antialiased;
}

.headerBack {
  display: none;
  background-color: rgb(31, 31, 36);
}

#goresults {
  display: none;
  grid-area: toresults;
}

.ruleHead {
  box-sizing: border-box;
  max-height: 100px;
  height: 100px;
  z-index: 1;
}

.ruleSubheader {
  padding: 5px;
  padding-left: 20px;
  background-color: #eee;
  position: sticky;
  top: 100px;
  border-bottom: 1px solid #ddd;
}

.header_check {
  flex-direction: row !important;
  margin-top: 7px;
}

.header_check input[type="checkbox"] {
  margin-right: 5px;
}

#pagecontrol {
  margin-top: 20px;
  padding-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pagination {
  min-height: 25px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.pageback,
.pageforward {
  font-size: 1.2rem;
  width: 20px;
  height: 20px;
  margin: 0 10px 0 10px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
  text-align: center;
  line-height: 20px;
  border-radius: 20px;
  opacity: 0;
  -moz-user-select: none;
  -webkit-user-select: none;
}

.resCount {
  margin-top: 0px;
  font-size: 0.8rem;
}

.vis {
  opacity: 1;
  cursor: pointer;
}

.h2 {
  font-weight: 500;
  font-size: 1.5rem;
  z-index: 2;
}

.bodyt,
.header_check,
.explain details summary,
.explain details,
.explain {
  color: #333;
}

.inset {
  box-sizing: border-box;
  border-bottom: 1px ridge rgba(0, 0, 0, 0.2);
}

.inset * {
  cursor: pointer;
}

.inset .inset_item {
  border-bottom: 2px dashed rgba(0, 0, 0, 0.1);
  transition: 0.1s ease;
  box-shadow: inset 0px 0px 0px 0px #0366d6;
}

.inset .inset_item:hover {
  background-color: #f1f8ff;
  box-shadow: inset 6px 0px 0px 0px #0366d6;
}

.inset_item:last-of-type {
  border-bottom: none;
}

#app {
  display: grid;
  grid-template-columns: 375px 1fr;
  grid-template-rows: 40px 1fr;
  gap: 0px 0px;
  overflow-y: hidden;
  grid-template-areas: "header header" "sidebar results";
}

.header {
  grid-area: header;
  background-color: rgb(31, 31, 36);
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: max-content 1fr max-content;
  grid-template-areas: "brown main info";
  justify-content: space-between;
  padding: 10px;
}

.header * {
  color: white;
  text-decoration: none;
  text-align: center;
}

.brown {
  grid-area: brown;
}

.main_logo {
  font-size: 1.2rem;
  font-weight: bold;
  grid-area: main;
}

.info {
  grid-area: info;
}

.sidebar {
  grid-area: sidebar;
  overflow: hidden;
  padding: 0 0 0 0;
  overflow-y: scroll;
  border-right: 1px solid rgba(0, 0, 0, 0.1);
}

.backButton {
  color: white;
  font-size: 1.7rem;
  font-weight: bold;
}

#rule_checkboxes {
  display: block;
}

.rule_checkbox {
  display: grid;
  background-color: #ffffff;
  grid-template-columns: 30px 1fr;
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  box-sizing: border-box;
  padding: 10px 17px 10px 15px;
  transition: 0.1s ease;
  box-shadow: inset 0px 0px 0px 0px yellowgreen;
}

.rule_checkbox.active {
  box-shadow: inset 9px 0px 0px 0px yellowgreen !important;
  background-color: #f9fff1 !important;
}

.rule_checkbox div.check_container {
  grid-area: 1 / 1 / 2 / 2;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  transition: 0.1s ease;
}

.providing:hover,
.opts:hover {
  background-color: white !important;
}

.rule_checkbox .desc {
  grid-area: 1 / 2 / 2 / 3;
}

.opts.single {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  border-bottom: none;
}

.single.available {
  border-bottom: 1px dashed #ddd;
}

.full.opts {
  padding-bottom: 0;
}

.full.available.opts {
  max-height: unset;
  padding-top: 0px;
  padding-bottom: 10px;
}

.single .desc {
  margin-top: 12px;
}

.rule_checkbox .desc .title {
  font-size: 1em;
  font-weight: 500;
  margin-bottom: 4px;
}

.bodyt {
  font-size: 0.85rem;
  margin-top: 3px;
}

.bodyt.sub,
.header_check {
  font-size: 0.85em;
  display: flex;
  flex-direction: column;
}

.stick {
  position: sticky;
  top: 0;
}

select {
  display: block;
  font-size: 0.8em;
  color: #444;
  line-height: 1.3;
  padding: 0.4em 1.2em 0.3em 0.6em;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  margin: 0;
  border: 1px solid #aaa;
  border-radius: 0.3em;
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E"),
    linear-gradient(to bottom, #ffffff 0%, #e5e5e5 100%);
  background-repeat: no-repeat, repeat;
  background-position: right 0.7em top 50%, 0 0;
  background-size: 0.65em auto, 100%;
}

.info {
  height: 100%;
  padding: 0 5px 0 5px;
  line-height: 100%;
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
}

.h2stick {
  padding-left: 20px;
  background-color: #f0f0f0;
  padding-bottom: 10px;
  border-bottom: 3px groove rgba(0, 0, 0, 0.15);
  box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.05);
  top: 0px;
}

.h2stick .h2 {
  padding-top: 10px;
}

.opts {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  max-height: 0;
  transition: 0.1s ease;
  overflow: hidden;
  border-color: none !important;
  padding: 0;
}

.explain {
  margin-top: 5px;
}

.explainer {
  margin-left: 15px;
  margin-top: 7px;
  line-height: 120%;
}

.available.opts {
  padding: 0.6em 1em 1.12em 2.7em;
  height: auto;
}

.results {
  background-color: #fafafa;
  display: flex;
  padding-top: 10px;
  padding-bottom: 20px;
  overflow: scroll;
  box-sizing: border-box;
  flex-direction: column;
  grid-area: results;
  align-items: center;
  justify-content: flex-start;
}

.opts * {
  opacity: 1;
  margin: 4px;
}

.opts input {
  outline: none;
  background: none;
  border: none;
  cursor: text;
  padding: 5px;
  border-bottom: 2px solid #0366d6;
  background-color: #f1f8ff;
  font-size: 0.9rem;
  text-align: center;
  height: 100%;
  color: #014b9e;
  line-height: 100%;
}

.inset .inset_item.no-bottom {
  border-bottom: none;
}

#ruleLimitNumbInput {
  width: 40px;
  color: #0366d6;
  border: none;
  text-align: center;
  padding: 1px;
  border-bottom: 2px solid #0366d6;
  background-color: #f1f8ff;
  font-size: 0.9rem;
}

.single.available.nobottom {
  border-bottom: none;
}

.warn {
  color: firebrick;
  text-decoration: underline;
  margin-top: 10px;
}

@media only screen and (max-width: 700px) {
  .header {
    grid-area: headerSidebar;
  }
  .headerBack {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    padding-left: 15px;
    grid-area: headerResults;
  }
  .brown {
    display: none;
  }
  html,
  body {
    overflow-x: hidden;
    overflow-y: scroll;
  }
  #app {
    width: 200%;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: 40px 1fr 80px;
    grid-column-gap: 0px;
    grid-row-gap: 0px;
    left: 0;
    overflow: hidden;
    grid-template-areas: "headerSidebar headerResults" "sidebar results" "toresults results" !important;
  }
  #app.showresults {
    margin-left: -100%;
  }
  .results {
    padding-top: 0;
    grid-area: results;
    overflow-y: scroll;
    padding-bottom: 0;
  }
  #goresults,
  #gofilter {
    display: flex;
    height: 100%;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    background-color: #e6e6e6;
    border-top: 2px solid #bbb;
    box-sizing: border-box;
    box-shadow: 0px -3px 5px 2px rgba(0, 0, 0, 0.15);
    cursor: pointer;
  }
  .gobutton {
    width: 90%;
    max-width: 230px;
    height: 45px;
    text-align: center;
    line-height: 44px;
    color: white;
    font-weight: bold;
    font-size: 1.3rem;
    border-radius: 30px;
    background-color: #0366d6;
  }
  .available.opts {
    padding-left: 0.2em;
    padding-right: 0.2em;
    font-size: 0.9rem;
    justify-content: center;
  }
  .bodyt {
    font-size: 0.85rem;
  }
  .stick {
    padding-right: 15px;
  }
}
</style>
