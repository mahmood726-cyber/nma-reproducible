# Usage: Rscript bench/build_corpus.R results/full/corpus.csv
# NMA validation corpus: every dataset shipped with the R package netmeta, as study contrasts built with
# pairwise() and the summary measure each dataset is documented with (Senn2013 and Linde2016 are already
# contrasts). Long format: dataset, sm, studlab, treat1, treat2, TE, seTE (netmeta's TE = treat1 - treat2).
# Contrasts that cannot be estimated (both arms without events) are left out, as netmeta needs them to be;
# this leaves Dong2013 with an incomplete three-arm study, which netmeta refuses.
suppressMessages(library(netmeta))
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "data/corpus.csv"
get_ds <- function(d) { e <- new.env(); data(list = d, package = "netmeta", envir = e); get(d, envir = e) }
contrasts_of <- function(nm) {
  x <- get_ds(nm)
  switch(nm,
    Baker2009 = list(pairwise(treatment, exac, total, studlab = study, data = x, sm = "OR"), "OR"),
    Dogliotti2014 = list(pairwise(treatment, stroke, total, studlab = study, data = x, sm = "OR"), "OR"),
    Dong2013 = list(pairwise(treatment, death, randomized, studlab = id, data = x, sm = "OR"), "OR"),
    Franchini2012 = , parkinson = list(pairwise(list(Treatment1, Treatment2, Treatment3), n = list(n1, n2, n3),
      mean = list(y1, y2, y3), sd = list(sd1, sd2, sd3), studlab = Study, data = x, sm = "MD"), "MD"),
    Gurusamy2011 = list(pairwise(treatment, death, n, studlab = study, data = x, sm = "OR"), "OR"),
    Linde2015 = list(pairwise(list(treatment1, treatment2, treatment3), event = list(resp1, resp2, resp3),
      n = list(n1, n2, n3), studlab = id, data = x, sm = "OR"), "OR"),
    Linde2016 = list(data.frame(studlab = x$id, treat1 = x$treat1, treat2 = x$treat2, TE = x$lnOR, seTE = x$selnOR), "OR"),
    Senn2013 = list(data.frame(studlab = x$studlab, treat1 = x$treat1, treat2 = x$treat2, TE = x$TE, seTE = x$seTE), "MD"),
    Stowe2010 = list(pairwise(list(t1, t2, t3), n = list(n1, n2, n3), mean = list(y1, y2, y3), sd = list(sd1, sd2, sd3),
      studlab = study, data = x, sm = "MD"), "MD"),
    Woods2010 = list(pairwise(treatment, event = r, n = N, studlab = author, data = x, sm = "OR"), "OR"),
    dietaryfat = list(pairwise(list(treat1, treat2, treat3), event = list(d1, d2, d3), time = list(years1, years2, years3),
      studlab = ID, data = x, sm = "IRR"), "IRR"),
    smokingcessation = list(pairwise(list(treat1, treat2, treat3), event = list(event1, event2, event3),
      n = list(n1, n2, n3), data = x, sm = "OR"), "OR"))
}
DS <- c("Baker2009", "Dogliotti2014", "Dong2013", "Franchini2012", "Gurusamy2011", "Linde2015", "Linde2016", "Senn2013",
        "Stowe2010", "Woods2010", "dietaryfat", "parkinson", "smokingcessation")
L <- lapply(DS, function(nm) {
  cs <- contrasts_of(nm); p <- as.data.frame(cs[[1]]); p <- p[is.finite(p$TE) & is.finite(p$seTE), ]
  data.frame(dataset = nm, sm = cs[[2]], studlab = as.character(p$studlab), treat1 = as.character(p$treat1),
             treat2 = as.character(p$treat2), TE = p$TE, seTE = p$seTE, stringsAsFactors = FALSE)
})
corpus <- do.call(rbind, L)
dir.create(dirname(out), showWarnings = FALSE, recursive = TRUE)
for (v in c("TE", "seTE")) corpus[[v]] <- sprintf("%.17g", corpus[[v]])  # round-trips every double exactly, on every platform
write.csv(corpus, out, row.names = FALSE, fileEncoding = "UTF-8", quote = 1:5)
cat(sprintf("corpus: %d datasets, %d studies, %d contrasts (netmeta %s)\n", length(DS),
            nrow(unique(corpus[, c("dataset", "studlab")])), nrow(corpus), packageVersion("netmeta")))
