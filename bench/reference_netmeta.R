# Usage: Rscript bench/reference_netmeta.R results/full/corpus.csv results/full/netmeta.jsonl
# Reference analyses with netmeta for every dataset in the corpus: netmeta() with its default
# DerSimonian-Laird tau^2, common and random effects, prediction intervals, and both random-effects CI
# methods ("classic", "t-dist"). A network netmeta refuses is recorded with its error message.
# Per fit: treatments; common- and random-effects league tables (estimate, SE, CI, p); prediction intervals
# (t with df of Q, only when df >= 2); Q, df, p; tau^2; I^2 with its CI; the design-based decomposition of
# Q (decomp.design); P-scores (netrank) with small values desirable and undesirable. One JSON object per
# dataset per line, numbers with 17 significant digits. The same analyses as allmeta's
# hub/shared/tests/_nma_parity_gen.R.
suppressMessages(library(netmeta))
args <- commandArgs(trailingOnly = TRUE)
corpus <- read.csv(args[1], stringsAsFactors = FALSE, colClasses = c(studlab = "character", treat1 = "character", treat2 = "character"))
out <- args[2]
num <- function(x) ifelse(is.finite(x), formatC(x, digits = 17, format = "g"), "null")
vec <- function(x) paste0("[", paste(num(as.numeric(x)), collapse = ","), "]")
str <- function(s) paste0('"', gsub('["\\\\\n\r\t]', " ", s), '"')
strv <- function(s) paste0("[", paste(vapply(as.character(s), str, ""), collapse = ","), "]")
obj <- function(...) { a <- list(...); a <- a[!vapply(a, is.null, NA)]; paste0("{", paste(paste0('"', names(a), '":', unlist(a)), collapse = ","), "}") }
mat <- function(M, trts) vec(t(M[trts, trts]))

fitone <- function(p, sm, ci) {
  f <- try(suppressWarnings(netmeta(TE, seTE, treat1, treat2, studlab, data = p, sm = sm, common = TRUE, random = TRUE,
                                    prediction = TRUE, method.random.ci = ci)), silent = TRUE)
  head <- list(method_random_ci = str(ci))
  if (inherits(f, "try-error")) return(do.call(obj, c(head, list(ok = "false", error = str(substr(as.character(f), 1, 200))))))
  tr <- f$trts
  dd <- try(decomp.design(f, warn = FALSE), silent = TRUE)
  qd <- if (inherits(dd, "try-error") || is.null(dd)) NULL else obj(Q = vec(dd$Q.decomp$Q), df = vec(dd$Q.decomp$df), pval = vec(dd$Q.decomp$pval))
  pd <- netrank(f, small.values = "desirable"); pu <- netrank(f, small.values = "undesirable")
  do.call(obj, c(head, list(ok = "true", trts = strv(tr), k = num(f$k), m = num(f$m), n = num(f$n),
    TE_common = mat(f$TE.common, tr), seTE_common = mat(f$seTE.common, tr), lower_common = mat(f$lower.common, tr),
    upper_common = mat(f$upper.common, tr), pval_common = mat(f$pval.common, tr),
    TE_random = mat(f$TE.random, tr), seTE_random = mat(f$seTE.random, tr), lower_random = mat(f$lower.random, tr),
    upper_random = mat(f$upper.random, tr), pval_random = mat(f$pval.random, tr),
    lower_predict = if (is.matrix(f$lower.predict)) mat(f$lower.predict, tr) else NULL,
    upper_predict = if (is.matrix(f$upper.predict)) mat(f$upper.predict, tr) else NULL,
    Q = num(f$Q), df_Q = num(f$df.Q), pval_Q = num(f$pval.Q), tau2 = num(f$tau2), tau = num(f$tau),
    I2 = num(f$I2), lower_I2 = num(f$lower.I2), upper_I2 = num(f$upper.I2), Q_decomp = qd,
    pscore_desirable = obj(common = vec(pd$ranking.common[tr]), random = vec(pd$ranking.random[tr])),
    pscore_undesirable = obj(common = vec(pu$ranking.common[tr]), random = vec(pu$ranking.random[tr])))))
}
lines <- character()
for (nm in unique(corpus$dataset)) {
  p <- corpus[corpus$dataset == nm, ]
  fits <- vapply(c("classic", "t-dist"), function(ci) fitone(p, p$sm[1], ci), "")
  lines <- c(lines, sprintf('{"dataset":"%s","sm":"%s","fits":[%s]}', nm, p$sm[1], paste(fits, collapse = ",")))
}
writeLines(lines, out, useBytes = TRUE)
cat(sprintf("netmeta %s (meta %s), R %s: %d datasets, %d analyses -> %s\n", packageVersion("netmeta"), packageVersion("meta"),
            getRversion(), length(lines), 2 * length(lines), out))
