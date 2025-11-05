# Mozilla Hire Stats

This is a fancy program which goal is to provide fancy statistics based on
country locations.  The goal is about challenging expectation based on
aggregated data that are hard to recall and could otherwise be the source of
miss-placed conclusions.

## How to use?

This program relies on a file named `hire_log.txt` placed in this repository,
and which should not be published.

This file should be layout as follows: (fictious data)

```
2025-12-20: :fr: :fr: :us: :flag-ca: :de: :flag-au: :flag-es:
2026-01-23: :fr: :us: :flag-ca: :de: :flag-au: :fr: :uk: :uk:
```

Then, after saving you can run the `hire_stats.py` file, which uses python 3, to
parse the `hire_log.txt` and generate fancy stats.

The result can be pipped into `xclip -i`, `xsel -ib` or `wl-copy` to put the result in the clipboard.

```
$ vim ./hire_log.txt
... edit and save ...
$ ./hire_stats.py | tee /dev/stderr | xclip -i
New Mozillian Flags: …
New Mozillian Flag Stats: …
New Mozillian Flag Stats (over the past year): …
New Mozillian Flag Stats (YoY constrast): …
```

## Understanting Stats

### New Flags

This simply echo the last entry of `hire_log.txt`.

### New Flags Stats

Count the number of each flag, divided by the total number of flags in the last
entry.

### New Flags Stats (YTD)

For all entries since the 1st of January, count the number of each flag, divided by the total
number of flags in this period.

### New Flags Stats (over the past year)

For the last 12 months, count the number of each flag, divided by the total
number of flags in this period.

### New Flag Stats (YoY contrast)

Considering the past 12 months (`new`) period and the past 12 months preiod before that (`old`), we count the number of flags in each period and compute the contrast.

The contrast is expressed as `(new - old) / (new + old)`.

If there is an increase in the given region, `new` would be higher than `old`
and this would show up as a positive number. The contrast goes between `-100%`
to `+100%`. A large positive / negative value show a large variation, where as a
value close to `0%` highlight a lack of variations.

Thus, regions with a few flag over the whole years are likely to show very high
variations, which highlight a higher impact for the given region.