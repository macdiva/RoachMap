library('rjags')

binomial <- read.csv('data/binomial_roaches.tsv', header = FALSE, sep = '\t')

names(binomial) <- c('Zipcode', 'InspectionCount', 'RoachViolations')

binomial <- transform(binomial, Zipcode = factor(Zipcode))

zipcodes <- with(binomial, unique(Zipcode))

pseudo.events <- data.frame()

for (zipcode in zipcodes)
{
  pseudo.events <- rbind(pseudo.events,
                         with(subset(binomial, Zipcode == zipcode),
                              data.frame(Zipcode = rep(zipcode, InspectionCount),
                                         RoachFound = c(rep(1, RoachViolations),
                                                        rep(0, InspectionCount - RoachViolations)))))
}

N <- nrow(pseudo.events)
K <- length(unique(pseudo.events$Zipcode))
 
jags <- jags.model('model.bug',
                   data = list('zipcode' = as.numeric(pseudo.events$Zipcode),
                               'roach' = pseudo.events$RoachFound,
                               'N' = N,
                               'K' = K),
                   n.chains = 4,
                   n.adapt = 1000)

update(jags, 1000)

samples <- jags.samples(jags,
                        c('theta', 'alpha', 'beta'),
                        1000)

means <- data.frame(Zipcode = zipcodes, Theta = apply(samples$theta, 1, mean))

write.csv(means,
          file = 'jags_estimates.csv',
          row.names = FALSE)
