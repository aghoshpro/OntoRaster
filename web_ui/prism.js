/* PrismJS 1.29.0
https://prismjs.com/download.html#themes=prism&languages=markup+css+clike+javascript+bash+sparql+sql+turtle&plugins=line-highlight+line-numbers+highlight-keywords+autoloader+command-line+data-uri-highlight+match-braces */
var _self =
		"undefined" != typeof window
			? window
			: "undefined" != typeof WorkerGlobalScope &&
			  self instanceof WorkerGlobalScope
			? self
			: {},
	Prism = (function (e) {
		var n = /(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i,
			t = 0,
			r = {},
			a = {
				manual: e.Prism && e.Prism.manual,
				disableWorkerMessageHandler:
					e.Prism && e.Prism.disableWorkerMessageHandler,
				util: {
					encode: function e(n) {
						return n instanceof i
							? new i(n.type, e(n.content), n.alias)
							: Array.isArray(n)
							? n.map(e)
							: n
									.replace(/&/g, "&amp;")
									.replace(/</g, "&lt;")
									.replace(/\u00a0/g, " ");
					},
					type: function (e) {
						return Object.prototype.toString.call(e).slice(8, -1);
					},
					objId: function (e) {
						return (
							e.__id || Object.defineProperty(e, "__id", { value: ++t }), e.__id
						);
					},
					clone: function e(n, t) {
						var r, i;
						switch (((t = t || {}), a.util.type(n))) {
							case "Object":
								if (((i = a.util.objId(n)), t[i])) return t[i];
								for (var l in ((r = {}), (t[i] = r), n))
									n.hasOwnProperty(l) && (r[l] = e(n[l], t));
								return r;
							case "Array":
								return (
									(i = a.util.objId(n)),
									t[i]
										? t[i]
										: ((r = []),
										  (t[i] = r),
										  n.forEach(function (n, a) {
												r[a] = e(n, t);
										  }),
										  r)
								);
							default:
								return n;
						}
					},
					getLanguage: function (e) {
						for (; e; ) {
							var t = n.exec(e.className);
							if (t) return t[1].toLowerCase();
							e = e.parentElement;
						}
						return "none";
					},
					setLanguage: function (e, t) {
						(e.className = e.className.replace(RegExp(n, "gi"), "")),
							e.classList.add("language-" + t);
					},
					currentScript: function () {
						if ("undefined" == typeof document) return null;
						if ("currentScript" in document) return document.currentScript;
						try {
							throw new Error();
						} catch (r) {
							var e = (/at [^(\r\n]*\((.*):[^:]+:[^:]+\)$/i.exec(r.stack) ||
								[])[1];
							if (e) {
								var n = document.getElementsByTagName("script");
								for (var t in n) if (n[t].src == e) return n[t];
							}
							return null;
						}
					},
					isActive: function (e, n, t) {
						for (var r = "no-" + n; e; ) {
							var a = e.classList;
							if (a.contains(n)) return !0;
							if (a.contains(r)) return !1;
							e = e.parentElement;
						}
						return !!t;
					},
				},
				languages: {
					plain: r,
					plaintext: r,
					text: r,
					txt: r,
					extend: function (e, n) {
						var t = a.util.clone(a.languages[e]);
						for (var r in n) t[r] = n[r];
						return t;
					},
					insertBefore: function (e, n, t, r) {
						var i = (r = r || a.languages)[e],
							l = {};
						for (var o in i)
							if (i.hasOwnProperty(o)) {
								if (o == n)
									for (var s in t) t.hasOwnProperty(s) && (l[s] = t[s]);
								t.hasOwnProperty(o) || (l[o] = i[o]);
							}
						var u = r[e];
						return (
							(r[e] = l),
							a.languages.DFS(a.languages, function (n, t) {
								t === u && n != e && (this[n] = l);
							}),
							l
						);
					},
					DFS: function e(n, t, r, i) {
						i = i || {};
						var l = a.util.objId;
						for (var o in n)
							if (n.hasOwnProperty(o)) {
								t.call(n, o, n[o], r || o);
								var s = n[o],
									u = a.util.type(s);
								"Object" !== u || i[l(s)]
									? "Array" !== u || i[l(s)] || ((i[l(s)] = !0), e(s, t, o, i))
									: ((i[l(s)] = !0), e(s, t, null, i));
							}
					},
				},
				plugins: {},
				highlightAll: function (e, n) {
					a.highlightAllUnder(document, e, n);
				},
				highlightAllUnder: function (e, n, t) {
					var r = {
						callback: t,
						container: e,
						selector:
							'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code',
					};
					a.hooks.run("before-highlightall", r),
						(r.elements = Array.prototype.slice.apply(
							r.container.querySelectorAll(r.selector)
						)),
						a.hooks.run("before-all-elements-highlight", r);
					for (var i, l = 0; (i = r.elements[l++]); )
						a.highlightElement(i, !0 === n, r.callback);
				},
				highlightElement: function (n, t, r) {
					var i = a.util.getLanguage(n),
						l = a.languages[i];
					a.util.setLanguage(n, i);
					var o = n.parentElement;
					o && "pre" === o.nodeName.toLowerCase() && a.util.setLanguage(o, i);
					var s = { element: n, language: i, grammar: l, code: n.textContent };
					function u(e) {
						(s.highlightedCode = e),
							a.hooks.run("before-insert", s),
							(s.element.innerHTML = s.highlightedCode),
							a.hooks.run("after-highlight", s),
							a.hooks.run("complete", s),
							r && r.call(s.element);
					}
					if (
						(a.hooks.run("before-sanity-check", s),
						(o = s.element.parentElement) &&
							"pre" === o.nodeName.toLowerCase() &&
							!o.hasAttribute("tabindex") &&
							o.setAttribute("tabindex", "0"),
						!s.code)
					)
						return a.hooks.run("complete", s), void (r && r.call(s.element));
					if ((a.hooks.run("before-highlight", s), s.grammar))
						if (t && e.Worker) {
							var c = new Worker(a.filename);
							(c.onmessage = function (e) {
								u(e.data);
							}),
								c.postMessage(
									JSON.stringify({
										language: s.language,
										code: s.code,
										immediateClose: !0,
									})
								);
						} else u(a.highlight(s.code, s.grammar, s.language));
					else u(a.util.encode(s.code));
				},
				highlight: function (e, n, t) {
					var r = { code: e, grammar: n, language: t };
					if ((a.hooks.run("before-tokenize", r), !r.grammar))
						throw new Error(
							'The language "' + r.language + '" has no grammar.'
						);
					return (
						(r.tokens = a.tokenize(r.code, r.grammar)),
						a.hooks.run("after-tokenize", r),
						i.stringify(a.util.encode(r.tokens), r.language)
					);
				},
				tokenize: function (e, n) {
					var t = n.rest;
					if (t) {
						for (var r in t) n[r] = t[r];
						delete n.rest;
					}
					var a = new s();
					return (
						u(a, a.head, e),
						o(e, a, n, a.head, 0),
						(function (e) {
							for (var n = [], t = e.head.next; t !== e.tail; )
								n.push(t.value), (t = t.next);
							return n;
						})(a)
					);
				},
				hooks: {
					all: {},
					add: function (e, n) {
						var t = a.hooks.all;
						(t[e] = t[e] || []), t[e].push(n);
					},
					run: function (e, n) {
						var t = a.hooks.all[e];
						if (t && t.length) for (var r, i = 0; (r = t[i++]); ) r(n);
					},
				},
				Token: i,
			};
		function i(e, n, t, r) {
			(this.type = e),
				(this.content = n),
				(this.alias = t),
				(this.length = 0 | (r || "").length);
		}
		function l(e, n, t, r) {
			e.lastIndex = n;
			var a = e.exec(t);
			if (a && r && a[1]) {
				var i = a[1].length;
				(a.index += i), (a[0] = a[0].slice(i));
			}
			return a;
		}
		function o(e, n, t, r, s, g) {
			for (var f in t)
				if (t.hasOwnProperty(f) && t[f]) {
					var h = t[f];
					h = Array.isArray(h) ? h : [h];
					for (var d = 0; d < h.length; ++d) {
						if (g && g.cause == f + "," + d) return;
						var v = h[d],
							p = v.inside,
							m = !!v.lookbehind,
							y = !!v.greedy,
							k = v.alias;
						if (y && !v.pattern.global) {
							var x = v.pattern.toString().match(/[imsuy]*$/)[0];
							v.pattern = RegExp(v.pattern.source, x + "g");
						}
						for (
							var b = v.pattern || v, w = r.next, A = s;
							w !== n.tail && !(g && A >= g.reach);
							A += w.value.length, w = w.next
						) {
							var E = w.value;
							if (n.length > e.length) return;
							if (!(E instanceof i)) {
								var P,
									L = 1;
								if (y) {
									if (!(P = l(b, A, e, m)) || P.index >= e.length) break;
									var S = P.index,
										O = P.index + P[0].length,
										j = A;
									for (j += w.value.length; S >= j; )
										j += (w = w.next).value.length;
									if (((A = j -= w.value.length), w.value instanceof i))
										continue;
									for (
										var C = w;
										C !== n.tail && (j < O || "string" == typeof C.value);
										C = C.next
									)
										L++, (j += C.value.length);
									L--, (E = e.slice(A, j)), (P.index -= A);
								} else if (!(P = l(b, 0, E, m))) continue;
								S = P.index;
								var N = P[0],
									_ = E.slice(0, S),
									M = E.slice(S + N.length),
									W = A + E.length;
								g && W > g.reach && (g.reach = W);
								var z = w.prev;
								if (
									(_ && ((z = u(n, z, _)), (A += _.length)),
									c(n, z, L),
									(w = u(n, z, new i(f, p ? a.tokenize(N, p) : N, k, N))),
									M && u(n, w, M),
									L > 1)
								) {
									var I = { cause: f + "," + d, reach: W };
									o(e, n, t, w.prev, A, I),
										g && I.reach > g.reach && (g.reach = I.reach);
								}
							}
						}
					}
				}
		}
		function s() {
			var e = { value: null, prev: null, next: null },
				n = { value: null, prev: e, next: null };
			(e.next = n), (this.head = e), (this.tail = n), (this.length = 0);
		}
		function u(e, n, t) {
			var r = n.next,
				a = { value: t, prev: n, next: r };
			return (n.next = a), (r.prev = a), e.length++, a;
		}
		function c(e, n, t) {
			for (var r = n.next, a = 0; a < t && r !== e.tail; a++) r = r.next;
			(n.next = r), (r.prev = n), (e.length -= a);
		}
		if (
			((e.Prism = a),
			(i.stringify = function e(n, t) {
				if ("string" == typeof n) return n;
				if (Array.isArray(n)) {
					var r = "";
					return (
						n.forEach(function (n) {
							r += e(n, t);
						}),
						r
					);
				}
				var i = {
						type: n.type,
						content: e(n.content, t),
						tag: "span",
						classes: ["token", n.type],
						attributes: {},
						language: t,
					},
					l = n.alias;
				l &&
					(Array.isArray(l)
						? Array.prototype.push.apply(i.classes, l)
						: i.classes.push(l)),
					a.hooks.run("wrap", i);
				var o = "";
				for (var s in i.attributes)
					o +=
						" " +
						s +
						'="' +
						(i.attributes[s] || "").replace(/"/g, "&quot;") +
						'"';
				return (
					"<" +
					i.tag +
					' class="' +
					i.classes.join(" ") +
					'"' +
					o +
					">" +
					i.content +
					"</" +
					i.tag +
					">"
				);
			}),
			!e.document)
		)
			return e.addEventListener
				? (a.disableWorkerMessageHandler ||
						e.addEventListener(
							"message",
							function (n) {
								var t = JSON.parse(n.data),
									r = t.language,
									i = t.code,
									l = t.immediateClose;
								e.postMessage(a.highlight(i, a.languages[r], r)),
									l && e.close();
							},
							!1
						),
				  a)
				: a;
		var g = a.util.currentScript();
		function f() {
			a.manual || a.highlightAll();
		}
		if (
			(g &&
				((a.filename = g.src),
				g.hasAttribute("data-manual") && (a.manual = !0)),
			!a.manual)
		) {
			var h = document.readyState;
			"loading" === h || ("interactive" === h && g && g.defer)
				? document.addEventListener("DOMContentLoaded", f)
				: window.requestAnimationFrame
				? window.requestAnimationFrame(f)
				: window.setTimeout(f, 16);
		}
		return a;
	})(_self);
"undefined" != typeof module && module.exports && (module.exports = Prism),
	"undefined" != typeof global && (global.Prism = Prism);
(Prism.languages.markup = {
	comment: { pattern: /<!--(?:(?!<!--)[\s\S])*?-->/, greedy: !0 },
	prolog: { pattern: /<\?[\s\S]+?\?>/, greedy: !0 },
	doctype: {
		pattern:
			/<!DOCTYPE(?:[^>"'[\]]|"[^"]*"|'[^']*')+(?:\[(?:[^<"'\]]|"[^"]*"|'[^']*'|<(?!!--)|<!--(?:[^-]|-(?!->))*-->)*\]\s*)?>/i,
		greedy: !0,
		inside: {
			"internal-subset": {
				pattern: /(^[^\[]*\[)[\s\S]+(?=\]>$)/,
				lookbehind: !0,
				greedy: !0,
				inside: null,
			},
			string: { pattern: /"[^"]*"|'[^']*'/, greedy: !0 },
			punctuation: /^<!|>$|[[\]]/,
			"doctype-tag": /^DOCTYPE/i,
			name: /[^\s<>'"]+/,
		},
	},
	cdata: { pattern: /<!\[CDATA\[[\s\S]*?\]\]>/i, greedy: !0 },
	tag: {
		pattern:
			/<\/?(?!\d)[^\s>\/=$<%]+(?:\s(?:\s*[^\s>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))|(?=[\s/>])))+)?\s*\/?>/,
		greedy: !0,
		inside: {
			tag: {
				pattern: /^<\/?[^\s>\/]+/,
				inside: { punctuation: /^<\/?/, namespace: /^[^\s>\/:]+:/ },
			},
			"special-attr": [],
			"attr-value": {
				pattern: /=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+)/,
				inside: {
					punctuation: [
						{ pattern: /^=/, alias: "attr-equals" },
						{ pattern: /^(\s*)["']|["']$/, lookbehind: !0 },
					],
				},
			},
			punctuation: /\/?>/,
			"attr-name": {
				pattern: /[^\s>\/]+/,
				inside: { namespace: /^[^\s>\/:]+:/ },
			},
		},
	},
	entity: [
		{ pattern: /&[\da-z]{1,8};/i, alias: "named-entity" },
		/&#x?[\da-f]{1,8};/i,
	],
}),
	(Prism.languages.markup.tag.inside["attr-value"].inside.entity =
		Prism.languages.markup.entity),
	(Prism.languages.markup.doctype.inside["internal-subset"].inside =
		Prism.languages.markup),
	Prism.hooks.add("wrap", function (a) {
		"entity" === a.type &&
			(a.attributes.title = a.content.replace(/&amp;/, "&"));
	}),
	Object.defineProperty(Prism.languages.markup.tag, "addInlined", {
		value: function (a, e) {
			var s = {};
			(s["language-" + e] = {
				pattern: /(^<!\[CDATA\[)[\s\S]+?(?=\]\]>$)/i,
				lookbehind: !0,
				inside: Prism.languages[e],
			}),
				(s.cdata = /^<!\[CDATA\[|\]\]>$/i);
			var t = {
				"included-cdata": { pattern: /<!\[CDATA\[[\s\S]*?\]\]>/i, inside: s },
			};
			t["language-" + e] = { pattern: /[\s\S]+/, inside: Prism.languages[e] };
			var n = {};
			(n[a] = {
				pattern: RegExp(
					"(<__[^>]*>)(?:<!\\[CDATA\\[(?:[^\\]]|\\](?!\\]>))*\\]\\]>|(?!<!\\[CDATA\\[)[^])*?(?=</__>)".replace(
						/__/g,
						function () {
							return a;
						}
					),
					"i"
				),
				lookbehind: !0,
				greedy: !0,
				inside: t,
			}),
				Prism.languages.insertBefore("markup", "cdata", n);
		},
	}),
	Object.defineProperty(Prism.languages.markup.tag, "addAttribute", {
		value: function (a, e) {
			Prism.languages.markup.tag.inside["special-attr"].push({
				pattern: RegExp(
					"(^|[\"'\\s])(?:" +
						a +
						")\\s*=\\s*(?:\"[^\"]*\"|'[^']*'|[^\\s'\">=]+(?=[\\s>]))",
					"i"
				),
				lookbehind: !0,
				inside: {
					"attr-name": /^[^\s=]+/,
					"attr-value": {
						pattern: /=[\s\S]+/,
						inside: {
							value: {
								pattern: /(^=\s*(["']|(?!["'])))\S[\s\S]*(?=\2$)/,
								lookbehind: !0,
								alias: [e, "language-" + e],
								inside: Prism.languages[e],
							},
							punctuation: [{ pattern: /^=/, alias: "attr-equals" }, /"|'/],
						},
					},
				},
			});
		},
	}),
	(Prism.languages.html = Prism.languages.markup),
	(Prism.languages.mathml = Prism.languages.markup),
	(Prism.languages.svg = Prism.languages.markup),
	(Prism.languages.xml = Prism.languages.extend("markup", {})),
	(Prism.languages.ssml = Prism.languages.xml),
	(Prism.languages.atom = Prism.languages.xml),
	(Prism.languages.rss = Prism.languages.xml);
!(function (s) {
	var e =
		/(?:"(?:\\(?:\r\n|[\s\S])|[^"\\\r\n])*"|'(?:\\(?:\r\n|[\s\S])|[^'\\\r\n])*')/;
	(s.languages.css = {
		comment: /\/\*[\s\S]*?\*\//,
		atrule: {
			pattern: RegExp(
				"@[\\w-](?:[^;{\\s\"']|\\s+(?!\\s)|" + e.source + ")*?(?:;|(?=\\s*\\{))"
			),
			inside: {
				rule: /^@[\w-]+/,
				"selector-function-argument": {
					pattern:
						/(\bselector\s*\(\s*(?![\s)]))(?:[^()\s]|\s+(?![\s)])|\((?:[^()]|\([^()]*\))*\))+(?=\s*\))/,
					lookbehind: !0,
					alias: "selector",
				},
				keyword: {
					pattern: /(^|[^\w-])(?:and|not|only|or)(?![\w-])/,
					lookbehind: !0,
				},
			},
		},
		url: {
			pattern: RegExp(
				"\\burl\\((?:" + e.source + "|(?:[^\\\\\r\n()\"']|\\\\[^])*)\\)",
				"i"
			),
			greedy: !0,
			inside: {
				function: /^url/i,
				punctuation: /^\(|\)$/,
				string: { pattern: RegExp("^" + e.source + "$"), alias: "url" },
			},
		},
		selector: {
			pattern: RegExp(
				"(^|[{}\\s])[^{}\\s](?:[^{};\"'\\s]|\\s+(?![\\s{])|" +
					e.source +
					")*(?=\\s*\\{)"
			),
			lookbehind: !0,
		},
		string: { pattern: e, greedy: !0 },
		property: {
			pattern:
				/(^|[^-\w\xA0-\uFFFF])(?!\s)[-_a-z\xA0-\uFFFF](?:(?!\s)[-\w\xA0-\uFFFF])*(?=\s*:)/i,
			lookbehind: !0,
		},
		important: /!important\b/i,
		function: { pattern: /(^|[^-a-z0-9])[-a-z0-9]+(?=\()/i, lookbehind: !0 },
		punctuation: /[(){};:,]/,
	}),
		(s.languages.css.atrule.inside.rest = s.languages.css);
	var t = s.languages.markup;
	t && (t.tag.addInlined("style", "css"), t.tag.addAttribute("style", "css"));
})(Prism);
Prism.languages.clike = {
	comment: [
		{ pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/, lookbehind: !0, greedy: !0 },
		{ pattern: /(^|[^\\:])\/\/.*/, lookbehind: !0, greedy: !0 },
	],
	string: {
		pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
		greedy: !0,
	},
	"class-name": {
		pattern:
			/(\b(?:class|extends|implements|instanceof|interface|new|trait)\s+|\bcatch\s+\()[\w.\\]+/i,
		lookbehind: !0,
		inside: { punctuation: /[.\\]/ },
	},
	keyword:
		/\b(?:break|catch|continue|do|else|finally|for|function|if|in|instanceof|new|null|return|throw|try|while)\b/,
	boolean: /\b(?:false|true)\b/,
	function: /\b\w+(?=\()/,
	number: /\b0x[\da-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?/i,
	operator: /[<>]=?|[!=]=?=?|--?|\+\+?|&&?|\|\|?|[?*/~^%]/,
	punctuation: /[{}[\];(),.:]/,
};
(Prism.languages.javascript = Prism.languages.extend("clike", {
	"class-name": [
		Prism.languages.clike["class-name"],
		{
			pattern:
				/(^|[^$\w\xA0-\uFFFF])(?!\s)[_$A-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\.(?:constructor|prototype))/,
			lookbehind: !0,
		},
	],
	keyword: [
		{ pattern: /((?:^|\})\s*)catch\b/, lookbehind: !0 },
		{
			pattern:
				/(^|[^.]|\.\.\.\s*)\b(?:as|assert(?=\s*\{)|async(?=\s*(?:function\b|\(|[$\w\xA0-\uFFFF]|$))|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally(?=\s*(?:\{|$))|for|from(?=\s*(?:['"]|$))|function|(?:get|set)(?=\s*(?:[#\[$\w\xA0-\uFFFF]|$))|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)\b/,
			lookbehind: !0,
		},
	],
	function:
		/#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*(?:\.\s*(?:apply|bind|call)\s*)?\()/,
	number: {
		pattern: RegExp(
			"(^|[^\\w$])(?:NaN|Infinity|0[bB][01]+(?:_[01]+)*n?|0[oO][0-7]+(?:_[0-7]+)*n?|0[xX][\\dA-Fa-f]+(?:_[\\dA-Fa-f]+)*n?|\\d+(?:_\\d+)*n|(?:\\d+(?:_\\d+)*(?:\\.(?:\\d+(?:_\\d+)*)?)?|\\.\\d+(?:_\\d+)*)(?:[Ee][+-]?\\d+(?:_\\d+)*)?)(?![\\w$])"
		),
		lookbehind: !0,
	},
	operator:
		/--|\+\+|\*\*=?|=>|&&=?|\|\|=?|[!=]==|<<=?|>>>?=?|[-+*/%&|^!=<>]=?|\.{3}|\?\?=?|\?\.?|[~:]/,
})),
	(Prism.languages.javascript["class-name"][0].pattern =
		/(\b(?:class|extends|implements|instanceof|interface|new)\s+)[\w.\\]+/),
	Prism.languages.insertBefore("javascript", "keyword", {
		regex: {
			pattern: RegExp(
				"((?:^|[^$\\w\\xA0-\\uFFFF.\"'\\])\\s]|\\b(?:return|yield))\\s*)/(?:(?:\\[(?:[^\\]\\\\\r\n]|\\\\.)*\\]|\\\\.|[^/\\\\\\[\r\n])+/[dgimyus]{0,7}|(?:\\[(?:[^[\\]\\\\\r\n]|\\\\.|\\[(?:[^[\\]\\\\\r\n]|\\\\.|\\[(?:[^[\\]\\\\\r\n]|\\\\.)*\\])*\\])*\\]|\\\\.|[^/\\\\\\[\r\n])+/[dgimyus]{0,7}v[dgimyus]{0,7})(?=(?:\\s|/\\*(?:[^*]|\\*(?!/))*\\*/)*(?:$|[\r\n,.;:})\\]]|//))"
			),
			lookbehind: !0,
			greedy: !0,
			inside: {
				"regex-source": {
					pattern: /^(\/)[\s\S]+(?=\/[a-z]*$)/,
					lookbehind: !0,
					alias: "language-regex",
					inside: Prism.languages.regex,
				},
				"regex-delimiter": /^\/|\/$/,
				"regex-flags": /^[a-z]+$/,
			},
		},
		"function-variable": {
			pattern:
				/#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*[=:]\s*(?:async\s*)?(?:\bfunction\b|(?:\((?:[^()]|\([^()]*\))*\)|(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)\s*=>))/,
			alias: "function",
		},
		parameter: [
			{
				pattern:
					/(function(?:\s+(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)?\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\))/,
				lookbehind: !0,
				inside: Prism.languages.javascript,
			},
			{
				pattern:
					/(^|[^$\w\xA0-\uFFFF])(?!\s)[_$a-z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*=>)/i,
				lookbehind: !0,
				inside: Prism.languages.javascript,
			},
			{
				pattern:
					/(\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*=>)/,
				lookbehind: !0,
				inside: Prism.languages.javascript,
			},
			{
				pattern:
					/((?:\b|\s|^)(?!(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)(?![$\w\xA0-\uFFFF]))(?:(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*)\(\s*|\]\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*\{)/,
				lookbehind: !0,
				inside: Prism.languages.javascript,
			},
		],
		constant: /\b[A-Z](?:[A-Z_]|\dx?)*\b/,
	}),
	Prism.languages.insertBefore("javascript", "string", {
		hashbang: { pattern: /^#!.*/, greedy: !0, alias: "comment" },
		"template-string": {
			pattern:
				/`(?:\\[\s\S]|\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}|(?!\$\{)[^\\`])*`/,
			greedy: !0,
			inside: {
				"template-punctuation": { pattern: /^`|`$/, alias: "string" },
				interpolation: {
					pattern:
						/((?:^|[^\\])(?:\\{2})*)\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}/,
					lookbehind: !0,
					inside: {
						"interpolation-punctuation": {
							pattern: /^\$\{|\}$/,
							alias: "punctuation",
						},
						rest: Prism.languages.javascript,
					},
				},
				string: /[\s\S]+/,
			},
		},
		"string-property": {
			pattern:
				/((?:^|[,{])[ \t]*)(["'])(?:\\(?:\r\n|[\s\S])|(?!\2)[^\\\r\n])*\2(?=\s*:)/m,
			lookbehind: !0,
			greedy: !0,
			alias: "property",
		},
	}),
	Prism.languages.insertBefore("javascript", "operator", {
		"literal-property": {
			pattern:
				/((?:^|[,{])[ \t]*)(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*:)/m,
			lookbehind: !0,
			alias: "property",
		},
	}),
	Prism.languages.markup &&
		(Prism.languages.markup.tag.addInlined("script", "javascript"),
		Prism.languages.markup.tag.addAttribute(
			"on(?:abort|blur|change|click|composition(?:end|start|update)|dblclick|error|focus(?:in|out)?|key(?:down|up)|load|mouse(?:down|enter|leave|move|out|over|up)|reset|resize|scroll|select|slotchange|submit|unload|wheel)",
			"javascript"
		)),
	(Prism.languages.js = Prism.languages.javascript);
!(function (e) {
	var t =
			"\\b(?:BASH|BASHOPTS|BASH_ALIASES|BASH_ARGC|BASH_ARGV|BASH_CMDS|BASH_COMPLETION_COMPAT_DIR|BASH_LINENO|BASH_REMATCH|BASH_SOURCE|BASH_VERSINFO|BASH_VERSION|COLORTERM|COLUMNS|COMP_WORDBREAKS|DBUS_SESSION_BUS_ADDRESS|DEFAULTS_PATH|DESKTOP_SESSION|DIRSTACK|DISPLAY|EUID|GDMSESSION|GDM_LANG|GNOME_KEYRING_CONTROL|GNOME_KEYRING_PID|GPG_AGENT_INFO|GROUPS|HISTCONTROL|HISTFILE|HISTFILESIZE|HISTSIZE|HOME|HOSTNAME|HOSTTYPE|IFS|INSTANCE|JOB|LANG|LANGUAGE|LC_ADDRESS|LC_ALL|LC_IDENTIFICATION|LC_MEASUREMENT|LC_MONETARY|LC_NAME|LC_NUMERIC|LC_PAPER|LC_TELEPHONE|LC_TIME|LESSCLOSE|LESSOPEN|LINES|LOGNAME|LS_COLORS|MACHTYPE|MAILCHECK|MANDATORY_PATH|NO_AT_BRIDGE|OLDPWD|OPTERR|OPTIND|ORBIT_SOCKETDIR|OSTYPE|PAPERSIZE|PATH|PIPESTATUS|PPID|PS1|PS2|PS3|PS4|PWD|RANDOM|REPLY|SECONDS|SELINUX_INIT|SESSION|SESSIONTYPE|SESSION_MANAGER|SHELL|SHELLOPTS|SHLVL|SSH_AUTH_SOCK|TERM|UID|UPSTART_EVENTS|UPSTART_INSTANCE|UPSTART_JOB|UPSTART_SESSION|USER|WINDOWID|XAUTHORITY|XDG_CONFIG_DIRS|XDG_CURRENT_DESKTOP|XDG_DATA_DIRS|XDG_GREETER_DATA_DIR|XDG_MENU_PREFIX|XDG_RUNTIME_DIR|XDG_SEAT|XDG_SEAT_PATH|XDG_SESSION_DESKTOP|XDG_SESSION_ID|XDG_SESSION_PATH|XDG_SESSION_TYPE|XDG_VTNR|XMODIFIERS)\\b",
		a = {
			pattern: /(^(["']?)\w+\2)[ \t]+\S.*/,
			lookbehind: !0,
			alias: "punctuation",
			inside: null,
		},
		n = {
			bash: a,
			environment: { pattern: RegExp("\\$" + t), alias: "constant" },
			variable: [
				{
					pattern: /\$?\(\([\s\S]+?\)\)/,
					greedy: !0,
					inside: {
						variable: [
							{ pattern: /(^\$\(\([\s\S]+)\)\)/, lookbehind: !0 },
							/^\$\(\(/,
						],
						number:
							/\b0x[\dA-Fa-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[Ee]-?\d+)?/,
						operator:
							/--|\+\+|\*\*=?|<<=?|>>=?|&&|\|\||[=!+\-*/%<>^&|]=?|[?~:]/,
						punctuation: /\(\(?|\)\)?|,|;/,
					},
				},
				{
					pattern: /\$\((?:\([^)]+\)|[^()])+\)|`[^`]+`/,
					greedy: !0,
					inside: { variable: /^\$\(|^`|\)$|`$/ },
				},
				{
					pattern: /\$\{[^}]+\}/,
					greedy: !0,
					inside: {
						operator: /:[-=?+]?|[!\/]|##?|%%?|\^\^?|,,?/,
						punctuation: /[\[\]]/,
						environment: {
							pattern: RegExp("(\\{)" + t),
							lookbehind: !0,
							alias: "constant",
						},
					},
				},
				/\$(?:\w+|[#?*!@$])/,
			],
			entity:
				/\\(?:[abceEfnrtv\\"]|O?[0-7]{1,3}|U[0-9a-fA-F]{8}|u[0-9a-fA-F]{4}|x[0-9a-fA-F]{1,2})/,
		};
	(e.languages.bash = {
		shebang: { pattern: /^#!\s*\/.*/, alias: "important" },
		comment: { pattern: /(^|[^"{\\$])#.*/, lookbehind: !0 },
		"function-name": [
			{
				pattern: /(\bfunction\s+)[\w-]+(?=(?:\s*\(?:\s*\))?\s*\{)/,
				lookbehind: !0,
				alias: "function",
			},
			{ pattern: /\b[\w-]+(?=\s*\(\s*\)\s*\{)/, alias: "function" },
		],
		"for-or-select": {
			pattern: /(\b(?:for|select)\s+)\w+(?=\s+in\s)/,
			alias: "variable",
			lookbehind: !0,
		},
		"assign-left": {
			pattern: /(^|[\s;|&]|[<>]\()\w+(?:\.\w+)*(?=\+?=)/,
			inside: {
				environment: {
					pattern: RegExp("(^|[\\s;|&]|[<>]\\()" + t),
					lookbehind: !0,
					alias: "constant",
				},
			},
			alias: "variable",
			lookbehind: !0,
		},
		parameter: {
			pattern: /(^|\s)-{1,2}(?:\w+:[+-]?)?\w+(?:\.\w+)*(?=[=\s]|$)/,
			alias: "variable",
			lookbehind: !0,
		},
		string: [
			{
				pattern: /((?:^|[^<])<<-?\s*)(\w+)\s[\s\S]*?(?:\r?\n|\r)\2/,
				lookbehind: !0,
				greedy: !0,
				inside: n,
			},
			{
				pattern: /((?:^|[^<])<<-?\s*)(["'])(\w+)\2\s[\s\S]*?(?:\r?\n|\r)\3/,
				lookbehind: !0,
				greedy: !0,
				inside: { bash: a },
			},
			{
				pattern:
					/(^|[^\\](?:\\\\)*)"(?:\\[\s\S]|\$\([^)]+\)|\$(?!\()|`[^`]+`|[^"\\`$])*"/,
				lookbehind: !0,
				greedy: !0,
				inside: n,
			},
			{ pattern: /(^|[^$\\])'[^']*'/, lookbehind: !0, greedy: !0 },
			{
				pattern: /\$'(?:[^'\\]|\\[\s\S])*'/,
				greedy: !0,
				inside: { entity: n.entity },
			},
		],
		environment: { pattern: RegExp("\\$?" + t), alias: "constant" },
		variable: n.variable,
		function: {
			pattern:
				/(^|[\s;|&]|[<>]\()(?:add|apropos|apt|apt-cache|apt-get|aptitude|aspell|automysqlbackup|awk|basename|bash|bc|bconsole|bg|bzip2|cal|cargo|cat|cfdisk|chgrp|chkconfig|chmod|chown|chroot|cksum|clear|cmp|column|comm|composer|cp|cron|crontab|csplit|curl|cut|date|dc|dd|ddrescue|debootstrap|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|docker|docker-compose|du|egrep|eject|env|ethtool|expand|expect|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|fuser|gawk|git|gparted|grep|groupadd|groupdel|groupmod|groups|grub-mkconfig|gzip|halt|head|hg|history|host|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|ip|java|jobs|join|kill|killall|less|link|ln|locate|logname|logrotate|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|lynx|make|man|mc|mdadm|mkconfig|mkdir|mke2fs|mkfifo|mkfs|mkisofs|mknod|mkswap|mmv|more|most|mount|mtools|mtr|mutt|mv|nano|nc|netstat|nice|nl|node|nohup|notify-send|npm|nslookup|op|open|parted|passwd|paste|pathchk|ping|pkill|pnpm|podman|podman-compose|popd|pr|printcap|printenv|ps|pushd|pv|quota|quotacheck|quotactl|ram|rar|rcp|reboot|remsync|rename|renice|rev|rm|rmdir|rpm|rsync|scp|screen|sdiff|sed|sendmail|seq|service|sftp|sh|shellcheck|shuf|shutdown|sleep|slocate|sort|split|ssh|stat|strace|su|sudo|sum|suspend|swapon|sync|sysctl|tac|tail|tar|tee|time|timeout|top|touch|tr|traceroute|tsort|tty|umount|uname|unexpand|uniq|units|unrar|unshar|unzip|update-grub|uptime|useradd|userdel|usermod|users|uudecode|uuencode|v|vcpkg|vdir|vi|vim|virsh|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yarn|yes|zenity|zip|zsh|zypper)(?=$|[)\s;|&])/,
			lookbehind: !0,
		},
		keyword: {
			pattern:
				/(^|[\s;|&]|[<>]\()(?:case|do|done|elif|else|esac|fi|for|function|if|in|select|then|until|while)(?=$|[)\s;|&])/,
			lookbehind: !0,
		},
		builtin: {
			pattern:
				/(^|[\s;|&]|[<>]\()(?:\.|:|alias|bind|break|builtin|caller|cd|command|continue|declare|echo|enable|eval|exec|exit|export|getopts|hash|help|let|local|logout|mapfile|printf|pwd|read|readarray|readonly|return|set|shift|shopt|source|test|times|trap|type|typeset|ulimit|umask|unalias|unset)(?=$|[)\s;|&])/,
			lookbehind: !0,
			alias: "class-name",
		},
		boolean: {
			pattern: /(^|[\s;|&]|[<>]\()(?:false|true)(?=$|[)\s;|&])/,
			lookbehind: !0,
		},
		"file-descriptor": { pattern: /\B&\d\b/, alias: "important" },
		operator: {
			pattern:
				/\d?<>|>\||\+=|=[=~]?|!=?|<<[<-]?|[&\d]?>>|\d[<>]&?|[<>][&=]?|&[>&]?|\|[&|]?/,
			inside: { "file-descriptor": { pattern: /^\d/, alias: "important" } },
		},
		punctuation: /\$?\(\(?|\)\)?|\.\.|[{}[\];\\]/,
		number: { pattern: /(^|\s)(?:[1-9]\d*|0)(?:[.,]\d+)?\b/, lookbehind: !0 },
	}),
		(a.inside = e.languages.bash);
	for (
		var s = [
				"comment",
				"function-name",
				"for-or-select",
				"assign-left",
				"parameter",
				"string",
				"environment",
				"function",
				"keyword",
				"builtin",
				"boolean",
				"file-descriptor",
				"operator",
				"punctuation",
				"number",
			],
			o = n.variable[1].inside,
			i = 0;
		i < s.length;
		i++
	)
		o[s[i]] = e.languages.bash[s[i]];
	(e.languages.sh = e.languages.bash), (e.languages.shell = e.languages.bash);
})(Prism);
(Prism.languages.turtle = {
	comment: { pattern: /#.*/, greedy: !0 },
	"multiline-string": {
		pattern:
			/"""(?:(?:""?)?(?:[^"\\]|\\.))*"""|'''(?:(?:''?)?(?:[^'\\]|\\.))*'''/,
		greedy: !0,
		alias: "string",
		inside: { comment: /#.*/ },
	},
	string: {
		pattern: /"(?:[^\\"\r\n]|\\.)*"|'(?:[^\\'\r\n]|\\.)*'/,
		greedy: !0,
	},
	url: {
		pattern:
			/<(?:[^\x00-\x20<>"{}|^`\\]|\\(?:u[\da-fA-F]{4}|U[\da-fA-F]{8}))*>/,
		greedy: !0,
		inside: { punctuation: /[<>]/ },
	},
	function: {
		pattern:
			/(?:(?![-.\d\xB7])[-.\w\xB7\xC0-\uFFFD]+)?:(?:(?![-.])(?:[-.:\w\xC0-\uFFFD]|%[\da-f]{2}|\\.)+)?/i,
		inside: {
			"local-name": { pattern: /([^:]*:)[\s\S]+/, lookbehind: !0 },
			prefix: { pattern: /[\s\S]+/, inside: { punctuation: /:/ } },
		},
	},
	number: /[+-]?\b\d+(?:\.\d*)?(?:e[+-]?\d+)?/i,
	punctuation: /[{}.,;()[\]]|\^\^/,
	boolean: /\b(?:false|true)\b/,
	keyword: [/(?:\ba|@prefix|@base)\b|=/, /\b(?:base|graph|prefix)\b/i],
	tag: { pattern: /@[a-z]+(?:-[a-z\d]+)*/i, inside: { punctuation: /@/ } },
}),
	(Prism.languages.trig = Prism.languages.turtle);
(Prism.languages.sparql = Prism.languages.extend("turtle", {
	boolean: /\b(?:false|true)\b/i,
	variable: { pattern: /[?$]\w+/, greedy: !0 },
})),
	Prism.languages.insertBefore("sparql", "punctuation", {
		keyword: [
			/\b(?:A|ADD|ALL|AS|ASC|ASK|BNODE|BY|CLEAR|CONSTRUCT|COPY|CREATE|DATA|DEFAULT|DELETE|DESC|DESCRIBE|DISTINCT|DROP|EXISTS|FILTER|FROM|GROUP|HAVING|INSERT|INTO|LIMIT|LOAD|MINUS|MOVE|NAMED|NOT|NOW|OFFSET|OPTIONAL|ORDER|RAND|REDUCED|SELECT|SEPARATOR|SERVICE|SILENT|STRUUID|UNION|USING|UUID|VALUES|WHERE)\b/i,
			/\b(?:ABS|AVG|BIND|BOUND|CEIL|COALESCE|CONCAT|CONTAINS|COUNT|DATATYPE|DAY|ENCODE_FOR_URI|FLOOR|GROUP_CONCAT|HOURS|IF|IRI|isBLANK|isIRI|isLITERAL|isNUMERIC|isURI|LANG|LANGMATCHES|LCASE|MAX|MD5|MIN|MINUTES|MONTH|REGEX|REPLACE|ROUND|sameTerm|SAMPLE|SECONDS|SHA1|SHA256|SHA384|SHA512|STR|STRAFTER|STRBEFORE|STRDT|STRENDS|STRLANG|STRLEN|STRSTARTS|SUBSTR|SUM|TIMEZONE|TZ|UCASE|URI|YEAR)\b(?=\s*\()/i,
			/\b(?:BASE|GRAPH|PREFIX)\b/i,
		],
	}),
	(Prism.languages.rq = Prism.languages.sparql);
Prism.languages.sql = {
	comment: {
		pattern: /(^|[^\\])(?:\/\*[\s\S]*?\*\/|(?:--|\/\/|#).*)/,
		lookbehind: !0,
	},
	variable: [
		{ pattern: /@(["'`])(?:\\[\s\S]|(?!\1)[^\\])+\1/, greedy: !0 },
		/@[\w.$]+/,
	],
	string: {
		pattern: /(^|[^@\\])("|')(?:\\[\s\S]|(?!\2)[^\\]|\2\2)*\2/,
		greedy: !0,
		lookbehind: !0,
	},
	identifier: {
		pattern: /(^|[^@\\])`(?:\\[\s\S]|[^`\\]|``)*`/,
		greedy: !0,
		lookbehind: !0,
		inside: { punctuation: /^`|`$/ },
	},
	function:
		/\b(?:AVG|COUNT|FIRST|FORMAT|LAST|LCASE|LEN|MAX|MID|MIN|MOD|NOW|ROUND|SUM|UCASE)(?=\s*\()/i,
	keyword:
		/\b(?:ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|CALL|CASCADED?|CASE|CHAIN|CHAR(?:ACTER|SET)?|CHECK(?:POINT)?|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMNS?|COMMENT|COMMIT(?:TED)?|COMPUTE|CONNECT|CONSISTENT|CONSTRAINT|CONTAINS(?:TABLE)?|CONTINUE|CONVERT|CREATE|CROSS|CURRENT(?:_DATE|_TIME|_TIMESTAMP|_USER)?|CURSOR|CYCLE|DATA(?:BASES?)?|DATE(?:TIME)?|DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITERS?|DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|DOUBLE|DROP|DUMMY|DUMP(?:FILE)?|DUPLICATE|ELSE(?:IF)?|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|ERRORS|ESCAPED?|EXCEPT|EXEC(?:UTE)?|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR(?: EACH ROW)?|FORCE|FOREIGN|FREETEXT(?:TABLE)?|FROM|FULL|FUNCTION|GEOMETRY(?:COLLECTION)?|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|HOLDLOCK|HOUR|IDENTITY(?:COL|_INSERT)?|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEYS?|KILL|LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONG(?:BLOB|TEXT)|LOOP|MATCH(?:ED)?|MEDIUM(?:BLOB|INT|TEXT)|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|MONTH|MULTI(?:LINESTRING|POINT|POLYGON)|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|NUMERIC|OFF?|OFFSETS?|ON|OPEN(?:DATASOURCE|QUERY|ROWSET)?|OPTIMIZE|OPTION(?:ALLY)?|ORDER|OUT(?:ER|FILE)?|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC(?:EDURE)?|PUBLIC|PURGE|QUICK|RAISERROR|READS?|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT(?:ABLE)?|REPLACE|REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURN(?:ING|S)?|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW(?:COUNT|GUIDCOL|S)?|RTREE|RULE|SAVE(?:POINT)?|SCHEMA|SECOND|SELECT|SERIAL(?:IZABLE)?|SESSION(?:_USER)?|SET(?:USER)?|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|START(?:ING)?|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLES?|TABLESPACE|TEMP(?:ORARY|TABLE)?|TERMINATED|TEXT(?:SIZE)?|THEN|TIME(?:STAMP)?|TINY(?:BLOB|INT|TEXT)|TOP?|TRAN(?:SACTIONS?)?|TRIGGER|TRUNCATE|TSEQUAL|TYPES?|UNBOUNDED|UNCOMMITTED|UNDEFINED|UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE(?:TEXT)?|USAGE|USE|USER|USING|VALUES?|VAR(?:BINARY|CHAR|CHARACTER|YING)|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH(?: ROLLUP|IN)?|WORK|WRITE(?:TEXT)?|YEAR)\b/i,
	boolean: /\b(?:FALSE|NULL|TRUE)\b/i,
	number: /\b0x[\da-f]+\b|\b\d+(?:\.\d*)?|\B\.\d+\b/i,
	operator:
		/[-+*\/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?|\b(?:AND|BETWEEN|DIV|ILIKE|IN|IS|LIKE|NOT|OR|REGEXP|RLIKE|SOUNDS LIKE|XOR)\b/i,
	punctuation: /[;[\]()`,.]/,
};
!(function () {
	if (
		"undefined" != typeof Prism &&
		"undefined" != typeof document &&
		document.querySelector
	) {
		var e,
			t = "line-numbers",
			i = "linkable-line-numbers",
			n = /\n(?!$)/g,
			r = !0;
		Prism.plugins.lineHighlight = {
			highlightLines: function (o, u, c) {
				var h = (u =
						"string" == typeof u ? u : o.getAttribute("data-line") || "")
						.replace(/\s+/g, "")
						.split(",")
						.filter(Boolean),
					d = +o.getAttribute("data-line-offset") || 0,
					f = (
						(function () {
							if (void 0 === e) {
								var t = document.createElement("div");
								(t.style.fontSize = "13px"),
									(t.style.lineHeight = "1.5"),
									(t.style.padding = "0"),
									(t.style.border = "0"),
									(t.innerHTML = "&nbsp;<br />&nbsp;"),
									document.body.appendChild(t),
									(e = 38 === t.offsetHeight),
									document.body.removeChild(t);
							}
							return e;
						})()
							? parseInt
							: parseFloat
					)(getComputedStyle(o).lineHeight),
					p = Prism.util.isActive(o, t),
					g = o.querySelector("code"),
					m = p ? o : g || o,
					v = [],
					y = g.textContent.match(n),
					b = y ? y.length + 1 : 1,
					A =
						g && m != g
							? (function (e, t) {
									var i = getComputedStyle(e),
										n = getComputedStyle(t);
									function r(e) {
										return +e.substr(0, e.length - 2);
									}
									return (
										t.offsetTop +
										r(n.borderTopWidth) +
										r(n.paddingTop) -
										r(i.paddingTop)
									);
							  })(o, g)
							: 0;
				h.forEach(function (e) {
					var t = e.split("-"),
						i = +t[0],
						n = +t[1] || i;
					if (!((n = Math.min(b + d, n)) < i)) {
						var r =
							o.querySelector('.line-highlight[data-range="' + e + '"]') ||
							document.createElement("div");
						if (
							(v.push(function () {
								r.setAttribute("aria-hidden", "true"),
									r.setAttribute("data-range", e),
									(r.className = (c || "") + " line-highlight");
							}),
							p && Prism.plugins.lineNumbers)
						) {
							var s = Prism.plugins.lineNumbers.getLine(o, i),
								l = Prism.plugins.lineNumbers.getLine(o, n);
							if (s) {
								var a = s.offsetTop + A + "px";
								v.push(function () {
									r.style.top = a;
								});
							}
							if (l) {
								var u = l.offsetTop - s.offsetTop + l.offsetHeight + "px";
								v.push(function () {
									r.style.height = u;
								});
							}
						} else
							v.push(function () {
								r.setAttribute("data-start", String(i)),
									n > i && r.setAttribute("data-end", String(n)),
									(r.style.top = (i - d - 1) * f + A + "px"),
									(r.textContent = new Array(n - i + 2).join(" \n"));
							});
						v.push(function () {
							r.style.width = o.scrollWidth + "px";
						}),
							v.push(function () {
								m.appendChild(r);
							});
					}
				});
				var P = o.id;
				if (p && Prism.util.isActive(o, i) && P) {
					l(o, i) ||
						v.push(function () {
							o.classList.add(i);
						});
					var E = parseInt(o.getAttribute("data-start") || "1");
					s(".line-numbers-rows > span", o).forEach(function (e, t) {
						var i = t + E;
						e.onclick = function () {
							var e = P + "." + i;
							(r = !1),
								(location.hash = e),
								setTimeout(function () {
									r = !0;
								}, 1);
						};
					});
				}
				return function () {
					v.forEach(a);
				};
			},
		};
		var o = 0;
		Prism.hooks.add("before-sanity-check", function (e) {
			var t = e.element.parentElement;
			if (u(t)) {
				var i = 0;
				s(".line-highlight", t).forEach(function (e) {
					(i += e.textContent.length), e.parentNode.removeChild(e);
				}),
					i &&
						/^(?: \n)+$/.test(e.code.slice(-i)) &&
						(e.code = e.code.slice(0, -i));
			}
		}),
			Prism.hooks.add("complete", function e(i) {
				var n = i.element.parentElement;
				if (u(n)) {
					clearTimeout(o);
					var r = Prism.plugins.lineNumbers,
						s = i.plugins && i.plugins.lineNumbers;
					l(n, t) && r && !s
						? Prism.hooks.add("line-numbers", e)
						: (Prism.plugins.lineHighlight.highlightLines(n)(),
						  (o = setTimeout(c, 1)));
				}
			}),
			window.addEventListener("hashchange", c),
			window.addEventListener("resize", function () {
				s("pre")
					.filter(u)
					.map(function (e) {
						return Prism.plugins.lineHighlight.highlightLines(e);
					})
					.forEach(a);
			});
	}
	function s(e, t) {
		return Array.prototype.slice.call((t || document).querySelectorAll(e));
	}
	function l(e, t) {
		return e.classList.contains(t);
	}
	function a(e) {
		e();
	}
	function u(e) {
		return !!(
			e &&
			/pre/i.test(e.nodeName) &&
			(e.hasAttribute("data-line") || (e.id && Prism.util.isActive(e, i)))
		);
	}
	function c() {
		var e = location.hash.slice(1);
		s(".temporary.line-highlight").forEach(function (e) {
			e.parentNode.removeChild(e);
		});
		var t = (e.match(/\.([\d,-]+)$/) || [, ""])[1];
		if (t && !document.getElementById(e)) {
			var i = e.slice(0, e.lastIndexOf(".")),
				n = document.getElementById(i);
			n &&
				(n.hasAttribute("data-line") || n.setAttribute("data-line", ""),
				Prism.plugins.lineHighlight.highlightLines(n, t, "temporary ")(),
				r &&
					document.querySelector(".temporary.line-highlight").scrollIntoView());
		}
	}
})();
!(function () {
	if ("undefined" != typeof Prism && "undefined" != typeof document) {
		var e = "line-numbers",
			n = /\n(?!$)/g,
			t = (Prism.plugins.lineNumbers = {
				getLine: function (n, t) {
					if ("PRE" === n.tagName && n.classList.contains(e)) {
						var i = n.querySelector(".line-numbers-rows");
						if (i) {
							var r = parseInt(n.getAttribute("data-start"), 10) || 1,
								s = r + (i.children.length - 1);
							t < r && (t = r), t > s && (t = s);
							var l = t - r;
							return i.children[l];
						}
					}
				},
				resize: function (e) {
					r([e]);
				},
				assumeViewportIndependence: !0,
			}),
			i = void 0;
		window.addEventListener("resize", function () {
			(t.assumeViewportIndependence && i === window.innerWidth) ||
				((i = window.innerWidth),
				r(
					Array.prototype.slice.call(
						document.querySelectorAll("pre.line-numbers")
					)
				));
		}),
			Prism.hooks.add("complete", function (t) {
				if (t.code) {
					var i = t.element,
						s = i.parentNode;
					if (
						s &&
						/pre/i.test(s.nodeName) &&
						!i.querySelector(".line-numbers-rows") &&
						Prism.util.isActive(i, e)
					) {
						i.classList.remove(e), s.classList.add(e);
						var l,
							o = t.code.match(n),
							a = o ? o.length + 1 : 1,
							u = new Array(a + 1).join("<span></span>");
						(l = document.createElement("span")).setAttribute(
							"aria-hidden",
							"true"
						),
							(l.className = "line-numbers-rows"),
							(l.innerHTML = u),
							s.hasAttribute("data-start") &&
								(s.style.counterReset =
									"linenumber " +
									(parseInt(s.getAttribute("data-start"), 10) - 1)),
							t.element.appendChild(l),
							r([s]),
							Prism.hooks.run("line-numbers", t);
					}
				}
			}),
			Prism.hooks.add("line-numbers", function (e) {
				(e.plugins = e.plugins || {}), (e.plugins.lineNumbers = !0);
			});
	}
	function r(e) {
		if (
			0 !=
			(e = e.filter(function (e) {
				var n,
					t = ((n = e),
					n
						? window.getComputedStyle
							? getComputedStyle(n)
							: n.currentStyle || null
						: null)["white-space"];
				return "pre-wrap" === t || "pre-line" === t;
			})).length
		) {
			var t = e
				.map(function (e) {
					var t = e.querySelector("code"),
						i = e.querySelector(".line-numbers-rows");
					if (t && i) {
						var r = e.querySelector(".line-numbers-sizer"),
							s = t.textContent.split(n);
						r ||
							(((r = document.createElement("span")).className =
								"line-numbers-sizer"),
							t.appendChild(r)),
							(r.innerHTML = "0"),
							(r.style.display = "block");
						var l = r.getBoundingClientRect().height;
						return (
							(r.innerHTML = ""),
							{
								element: e,
								lines: s,
								lineHeights: [],
								oneLinerHeight: l,
								sizer: r,
							}
						);
					}
				})
				.filter(Boolean);
			t.forEach(function (e) {
				var n = e.sizer,
					t = e.lines,
					i = e.lineHeights,
					r = e.oneLinerHeight;
				(i[t.length - 1] = void 0),
					t.forEach(function (e, t) {
						if (e && e.length > 1) {
							var s = n.appendChild(document.createElement("span"));
							(s.style.display = "block"), (s.textContent = e);
						} else i[t] = r;
					});
			}),
				t.forEach(function (e) {
					for (
						var n = e.sizer, t = e.lineHeights, i = 0, r = 0;
						r < t.length;
						r++
					)
						void 0 === t[r] &&
							(t[r] = n.children[i++].getBoundingClientRect().height);
				}),
				t.forEach(function (e) {
					var n = e.sizer,
						t = e.element.querySelector(".line-numbers-rows");
					(n.style.display = "none"),
						(n.innerHTML = ""),
						e.lineHeights.forEach(function (e, n) {
							t.children[n].style.height = e + "px";
						});
				});
		}
	}
})();
"undefined" != typeof Prism &&
	Prism.hooks.add("wrap", function (e) {
		"keyword" === e.type && e.classes.push("keyword-" + e.content);
	});
!(function () {
	if ("undefined" != typeof Prism && "undefined" != typeof document) {
		var e = {
				javascript: "clike",
				actionscript: "javascript",
				apex: ["clike", "sql"],
				arduino: "cpp",
				aspnet: ["markup", "csharp"],
				birb: "clike",
				bison: "c",
				c: "clike",
				csharp: "clike",
				cpp: "c",
				cfscript: "clike",
				chaiscript: ["clike", "cpp"],
				cilkc: "c",
				cilkcpp: "cpp",
				coffeescript: "javascript",
				crystal: "ruby",
				"css-extras": "css",
				d: "clike",
				dart: "clike",
				django: "markup-templating",
				ejs: ["javascript", "markup-templating"],
				etlua: ["lua", "markup-templating"],
				erb: ["ruby", "markup-templating"],
				fsharp: "clike",
				"firestore-security-rules": "clike",
				flow: "javascript",
				ftl: "markup-templating",
				gml: "clike",
				glsl: "c",
				go: "clike",
				gradle: "clike",
				groovy: "clike",
				haml: "ruby",
				handlebars: "markup-templating",
				haxe: "clike",
				hlsl: "c",
				idris: "haskell",
				java: "clike",
				javadoc: ["markup", "java", "javadoclike"],
				jolie: "clike",
				jsdoc: ["javascript", "javadoclike", "typescript"],
				"js-extras": "javascript",
				json5: "json",
				jsonp: "json",
				"js-templates": "javascript",
				kotlin: "clike",
				latte: ["clike", "markup-templating", "php"],
				less: "css",
				lilypond: "scheme",
				liquid: "markup-templating",
				markdown: "markup",
				"markup-templating": "markup",
				mongodb: "javascript",
				n4js: "javascript",
				objectivec: "c",
				opencl: "c",
				parser: "markup",
				php: "markup-templating",
				phpdoc: ["php", "javadoclike"],
				"php-extras": "php",
				plsql: "sql",
				processing: "clike",
				protobuf: "clike",
				pug: ["markup", "javascript"],
				purebasic: "clike",
				purescript: "haskell",
				qsharp: "clike",
				qml: "javascript",
				qore: "clike",
				racket: "scheme",
				cshtml: ["markup", "csharp"],
				jsx: ["markup", "javascript"],
				tsx: ["jsx", "typescript"],
				reason: "clike",
				ruby: "clike",
				sass: "css",
				scss: "css",
				scala: "java",
				"shell-session": "bash",
				smarty: "markup-templating",
				solidity: "clike",
				soy: "markup-templating",
				sparql: "turtle",
				sqf: "clike",
				squirrel: "clike",
				stata: ["mata", "java", "python"],
				"t4-cs": ["t4-templating", "csharp"],
				"t4-vb": ["t4-templating", "vbnet"],
				tap: "yaml",
				tt2: ["clike", "markup-templating"],
				textile: "markup",
				twig: "markup-templating",
				typescript: "javascript",
				v: "clike",
				vala: "clike",
				vbnet: "basic",
				velocity: "markup",
				wiki: "markup",
				xeora: "markup",
				"xml-doc": "markup",
				xquery: "markup",
			},
			a = {
				html: "markup",
				xml: "markup",
				svg: "markup",
				mathml: "markup",
				ssml: "markup",
				atom: "markup",
				rss: "markup",
				js: "javascript",
				g4: "antlr4",
				ino: "arduino",
				"arm-asm": "armasm",
				art: "arturo",
				adoc: "asciidoc",
				avs: "avisynth",
				avdl: "avro-idl",
				gawk: "awk",
				sh: "bash",
				shell: "bash",
				shortcode: "bbcode",
				rbnf: "bnf",
				oscript: "bsl",
				cs: "csharp",
				dotnet: "csharp",
				cfc: "cfscript",
				"cilk-c": "cilkc",
				"cilk-cpp": "cilkcpp",
				cilk: "cilkcpp",
				coffee: "coffeescript",
				conc: "concurnas",
				jinja2: "django",
				"dns-zone": "dns-zone-file",
				dockerfile: "docker",
				gv: "dot",
				eta: "ejs",
				xlsx: "excel-formula",
				xls: "excel-formula",
				gamemakerlanguage: "gml",
				po: "gettext",
				gni: "gn",
				ld: "linker-script",
				"go-mod": "go-module",
				hbs: "handlebars",
				mustache: "handlebars",
				hs: "haskell",
				idr: "idris",
				gitignore: "ignore",
				hgignore: "ignore",
				npmignore: "ignore",
				webmanifest: "json",
				kt: "kotlin",
				kts: "kotlin",
				kum: "kumir",
				tex: "latex",
				context: "latex",
				ly: "lilypond",
				emacs: "lisp",
				elisp: "lisp",
				"emacs-lisp": "lisp",
				md: "markdown",
				moon: "moonscript",
				n4jsd: "n4js",
				nani: "naniscript",
				objc: "objectivec",
				qasm: "openqasm",
				objectpascal: "pascal",
				px: "pcaxis",
				pcode: "peoplecode",
				plantuml: "plant-uml",
				pq: "powerquery",
				mscript: "powerquery",
				pbfasm: "purebasic",
				purs: "purescript",
				py: "python",
				qs: "qsharp",
				rkt: "racket",
				razor: "cshtml",
				rpy: "renpy",
				res: "rescript",
				robot: "robotframework",
				rb: "ruby",
				"sh-session": "shell-session",
				shellsession: "shell-session",
				smlnj: "sml",
				sol: "solidity",
				sln: "solution-file",
				rq: "sparql",
				sclang: "supercollider",
				t4: "t4-cs",
				trickle: "tremor",
				troy: "tremor",
				trig: "turtle",
				ts: "typescript",
				tsconfig: "typoscript",
				uscript: "unrealscript",
				uc: "unrealscript",
				url: "uri",
				vb: "visual-basic",
				vba: "visual-basic",
				webidl: "web-idl",
				mathematica: "wolfram",
				nb: "wolfram",
				wl: "wolfram",
				xeoracube: "xeora",
				yml: "yaml",
			},
			r = {},
			s = "components/",
			i = Prism.util.currentScript();
		if (i) {
			var t =
					/\bplugins\/autoloader\/prism-autoloader\.(?:min\.)?js(?:\?[^\r\n/]*)?$/i,
				c = /(^|\/)[\w-]+\.(?:min\.)?js(?:\?[^\r\n/]*)?$/i,
				l = i.getAttribute("data-autoloader-path");
			if (null != l) s = l.trim().replace(/\/?$/, "/");
			else {
				var p = i.src;
				t.test(p)
					? (s = p.replace(t, "components/"))
					: c.test(p) && (s = p.replace(c, "$1components/"));
			}
		}
		var n = (Prism.plugins.autoloader = {
			languages_path: s,
			use_minified: !0,
			loadLanguages: m,
		});
		Prism.hooks.add("complete", function (e) {
			var a = e.element,
				r = e.language;
			if (a && r && "none" !== r) {
				var s = (function (e) {
					var a = (e.getAttribute("data-dependencies") || "").trim();
					if (!a) {
						var r = e.parentElement;
						r &&
							"pre" === r.tagName.toLowerCase() &&
							(a = (r.getAttribute("data-dependencies") || "").trim());
					}
					return a ? a.split(/\s*,\s*/g) : [];
				})(a);
				/^diff-./i.test(r)
					? (s.push("diff"), s.push(r.substr("diff-".length)))
					: s.push(r),
					s.every(o) ||
						m(s, function () {
							Prism.highlightElement(a);
						});
			}
		});
	}
	function o(e) {
		if (e.indexOf("!") >= 0) return !1;
		if ((e = a[e] || e) in Prism.languages) return !0;
		var s = r[e];
		return s && !s.error && !1 === s.loading;
	}
	function m(s, i, t) {
		"string" == typeof s && (s = [s]);
		var c = s.length,
			l = 0,
			p = !1;
		function k() {
			p || (++l === c && i && i(s));
		}
		0 !== c
			? s.forEach(function (s) {
					!(function (s, i, t) {
						var c = s.indexOf("!") >= 0;
						function l() {
							var e = r[s];
							e || (e = r[s] = { callbacks: [] }),
								e.callbacks.push({ success: i, error: t }),
								!c && o(s)
									? u(s, "success")
									: !c && e.error
									? u(s, "error")
									: (!c && e.loading) ||
									  ((e.loading = !0),
									  (e.error = !1),
									  (function (e, a, r) {
											var s = document.createElement("script");
											(s.src = e),
												(s.async = !0),
												(s.onload = function () {
													document.body.removeChild(s), a && a();
												}),
												(s.onerror = function () {
													document.body.removeChild(s), r && r();
												}),
												document.body.appendChild(s);
									  })(
											(function (e) {
												return (
													n.languages_path +
													"prism-" +
													e +
													(n.use_minified ? ".min" : "") +
													".js"
												);
											})(s),
											function () {
												(e.loading = !1), u(s, "success");
											},
											function () {
												(e.loading = !1), (e.error = !0), u(s, "error");
											}
									  ));
						}
						s = s.replace("!", "");
						var p = e[(s = a[s] || s)];
						p && p.length ? m(p, l, t) : l();
					})(s, k, function () {
						p || ((p = !0), t && t(s));
					});
			  })
			: i && setTimeout(i, 0);
	}
	function u(e, a) {
		if (r[e]) {
			for (var s = r[e].callbacks, i = 0, t = s.length; i < t; i++) {
				var c = s[i][a];
				c && setTimeout(c, 0);
			}
			s.length = 0;
		}
	}
})();
!(function () {
	if ("undefined" != typeof Prism && "undefined" != typeof document) {
		var e = /(?:^|\s)command-line(?:\s|$)/,
			t = "command-line-prompt",
			n = "".startsWith
				? function (e, t) {
						return e.startsWith(t);
				  }
				: function (e, t) {
						return 0 === e.indexOf(t);
				  },
			a = "".endsWith
				? function (e, t) {
						return e.endsWith(t);
				  }
				: function (e, t) {
						var n = e.length;
						return e.substring(n - t.length, n) === t;
				  };
		Prism.hooks.add("before-highlight", function (i) {
			var o = r(i);
			if (!o.complete && i.code) {
				var s = i.element.parentElement;
				if (
					s &&
					/pre/i.test(s.nodeName) &&
					(e.test(s.className) || e.test(i.element.className))
				) {
					var l = i.element.querySelector("." + t);
					l && l.remove();
					var m = i.code.split("\n");
					o.numberOfLines = m.length;
					var u = (o.outputLines = []),
						c = s.getAttribute("data-output"),
						d = s.getAttribute("data-filter-output");
					if (null !== c)
						c.split(",").forEach(function (e) {
							var t = e.split("-"),
								n = parseInt(t[0], 10),
								a = 2 === t.length ? parseInt(t[1], 10) : n;
							if (!isNaN(n) && !isNaN(a)) {
								n < 1 && (n = 1), a > m.length && (a = m.length), a--;
								for (var r = --n; r <= a; r++) (u[r] = m[r]), (m[r] = "");
							}
						});
					else if (d)
						for (var p = 0; p < m.length; p++)
							n(m[p], d) && ((u[p] = m[p].slice(d.length)), (m[p] = ""));
					for (
						var f = (o.continuationLineIndicies = new Set()),
							h = s.getAttribute("data-continuation-str"),
							v = s.getAttribute("data-filter-continuation"),
							g = 0;
						g < m.length;
						g++
					) {
						var b = m[g];
						b &&
							(h && a(b, h) && f.add(g + 1),
							g > 0 && v && n(b, v) && ((m[g] = b.slice(v.length)), f.add(g)));
					}
					i.code = m.join("\n");
				} else o.complete = !0;
			} else o.complete = !0;
		}),
			Prism.hooks.add("before-insert", function (e) {
				var t = r(e);
				if (!t.complete) {
					for (
						var n = e.highlightedCode.split("\n"),
							a = t.outputLines || [],
							i = 0,
							o = n.length;
						i < o;
						i++
					)
						a.hasOwnProperty(i)
							? (n[i] =
									'<span class="token output">' +
									Prism.util.encode(a[i]) +
									"</span>")
							: (n[i] = '<span class="token command">' + n[i] + "</span>");
					e.highlightedCode = n.join("\n");
				}
			}),
			Prism.hooks.add("complete", function (n) {
				if (
					(function (e) {
						return "command-line" in (e.vars = e.vars || {});
					})(n)
				) {
					var a = r(n);
					if (!a.complete) {
						var i = n.element.parentElement;
						e.test(n.element.className) &&
							(n.element.className = n.element.className.replace(e, " ")),
							e.test(i.className) || (i.className += " command-line");
						var o,
							s = "",
							l = a.numberOfLines || 0,
							m = b("data-prompt", "");
						o =
							"" !== m
								? '<span data-prompt="' + m + '"></span>'
								: '<span data-user="' +
								  b("data-user", "user") +
								  '" data-host="' +
								  b("data-host", "localhost") +
								  '"></span>';
						for (
							var u = a.continuationLineIndicies || new Set(),
								c =
									'<span data-continuation-prompt="' +
									b("data-continuation-prompt", ">") +
									'"></span>',
								d = 0;
							d < l;
							d++
						)
							u.has(d) ? (s += c) : (s += o);
						var p = document.createElement("span");
						(p.className = t), (p.innerHTML = s);
						for (var f = a.outputLines || [], h = 0, v = f.length; h < v; h++)
							if (f.hasOwnProperty(h)) {
								var g = p.children[h];
								g.removeAttribute("data-user"),
									g.removeAttribute("data-host"),
									g.removeAttribute("data-prompt");
							}
						n.element.insertBefore(p, n.element.firstChild), (a.complete = !0);
					}
				}
				function b(e, t) {
					return (i.getAttribute(e) || t).replace(/"/g, "&quot");
				}
			});
	}
	function r(e) {
		var t = (e.vars = e.vars || {});
		return (t["command-line"] = t["command-line"] || {});
	}
})();
!(function () {
	if ("undefined" != typeof Prism) {
		var i = {
				pattern: /(.)\bdata:[^\/]+\/[^,]+,(?:(?!\1)[\s\S]|\\\1)+(?=\1)/,
				lookbehind: !0,
				inside: {
					"language-css": {
						pattern: /(data:[^\/]+\/(?:[^+,]+\+)?css,)[\s\S]+/,
						lookbehind: !0,
					},
					"language-javascript": {
						pattern: /(data:[^\/]+\/(?:[^+,]+\+)?javascript,)[\s\S]+/,
						lookbehind: !0,
					},
					"language-json": {
						pattern: /(data:[^\/]+\/(?:[^+,]+\+)?json,)[\s\S]+/,
						lookbehind: !0,
					},
					"language-markup": {
						pattern: /(data:[^\/]+\/(?:[^+,]+\+)?(?:html|xml),)[\s\S]+/,
						lookbehind: !0,
					},
				},
			},
			a = ["url", "attr-value", "string"];
		(Prism.plugins.dataURIHighlight = {
			processGrammar: function (n) {
				n &&
					!n["data-uri"] &&
					(Prism.languages.DFS(n, function (n, r, e) {
						a.indexOf(e) > -1 &&
							!Array.isArray(r) &&
							(r.pattern || (r = this[n] = { pattern: r }),
							(r.inside = r.inside || {}),
							"attr-value" == e
								? Prism.languages.insertBefore(
										"inside",
										r.inside["url-link"] ? "url-link" : "punctuation",
										{ "data-uri": i },
										r
								  )
								: r.inside["url-link"]
								? Prism.languages.insertBefore(
										"inside",
										"url-link",
										{ "data-uri": i },
										r
								  )
								: (r.inside["data-uri"] = i));
					}),
					(n["data-uri"] = i));
			},
		}),
			Prism.hooks.add("before-highlight", function (a) {
				if (i.pattern.test(a.code))
					for (var n in i.inside)
						if (
							i.inside.hasOwnProperty(n) &&
							!i.inside[n].inside &&
							i.inside[n].pattern.test(a.code)
						) {
							var r = n.match(/^language-(.+)/)[1];
							Prism.languages[r] &&
								(i.inside[n].inside = {
									rest:
										((e = Prism.languages[r]),
										Prism.plugins.autolinker &&
											Prism.plugins.autolinker.processGrammar(e),
										e),
								});
						}
				var e;
				Prism.plugins.dataURIHighlight.processGrammar(a.grammar);
			});
	}
})();
!(function () {
	if ("undefined" != typeof Prism && "undefined" != typeof document) {
		var e = { "(": ")", "[": "]", "{": "}" },
			t = { "(": "brace-round", "[": "brace-square", "{": "brace-curly" },
			n = { "${": "{" },
			r = 0,
			c = /^(pair-\d+-)(close|open)$/;
		Prism.hooks.add("complete", function (c) {
			var i = c.element,
				d = i.parentElement;
			if (d && "PRE" == d.tagName) {
				var u = [];
				if (
					(Prism.util.isActive(i, "match-braces") && u.push("(", "[", "{"),
					0 != u.length)
				) {
					d.__listenerAdded ||
						(d.addEventListener("mousedown", function () {
							var e = d.querySelector("code"),
								t = s("brace-selected");
							Array.prototype.slice
								.call(e.querySelectorAll("." + t))
								.forEach(function (e) {
									e.classList.remove(t);
								});
						}),
						Object.defineProperty(d, "__listenerAdded", { value: !0 }));
					var f = Array.prototype.slice.call(
							i.querySelectorAll("span." + s("token") + "." + s("punctuation"))
						),
						h = [];
					u.forEach(function (c) {
						for (
							var i = e[c], d = s(t[c]), u = [], p = [], v = 0;
							v < f.length;
							v++
						) {
							var m = f[v];
							if (0 == m.childElementCount) {
								var b = m.textContent;
								(b = n[b] || b) === c
									? (h.push({ index: v, open: !0, element: m }),
									  m.classList.add(d),
									  m.classList.add(s("brace-open")),
									  p.push(v))
									: b === i &&
									  (h.push({ index: v, open: !1, element: m }),
									  m.classList.add(d),
									  m.classList.add(s("brace-close")),
									  p.length && u.push([v, p.pop()]));
							}
						}
						u.forEach(function (e) {
							var t = "pair-" + r++ + "-",
								n = f[e[0]],
								c = f[e[1]];
							(n.id = t + "open"),
								(c.id = t + "close"),
								[n, c].forEach(function (e) {
									e.addEventListener("mouseenter", a),
										e.addEventListener("mouseleave", o),
										e.addEventListener("click", l);
								});
						});
					});
					var p = 0;
					h.sort(function (e, t) {
						return e.index - t.index;
					}),
						h.forEach(function (e) {
							e.open
								? (e.element.classList.add(s("brace-level-" + ((p % 12) + 1))),
								  p++)
								: ((p = Math.max(0, p - 1)),
								  e.element.classList.add(s("brace-level-" + ((p % 12) + 1))));
						});
				}
			}
		});
	}
	function s(e) {
		var t = Prism.plugins.customClass;
		return t ? t.apply(e, "none") : e;
	}
	function i(e) {
		var t = c.exec(e.id);
		return document.querySelector(
			"#" + t[1] + ("open" == t[2] ? "close" : "open")
		);
	}
	function a() {
		Prism.util.isActive(this, "brace-hover", !0) &&
			[this, i(this)].forEach(function (e) {
				e.classList.add(s("brace-hover"));
			});
	}
	function o() {
		[this, i(this)].forEach(function (e) {
			e.classList.remove(s("brace-hover"));
		});
	}
	function l() {
		Prism.util.isActive(this, "brace-select", !0) &&
			[this, i(this)].forEach(function (e) {
				e.classList.add(s("brace-selected"));
			});
	}
})();
