# Contributing
If you'd like to contribute, first of all, _thank you_!

I'm still thinking about the ideal workflow for this project, however I'd 
like to keep PM on GitHub for now. Please first discuss the change you wish
to make with the owners of this repository, ideally via issue, before making 
a change or opening a pull request. Further, if you see an issue you'd like
to work on, check the discussion on it to make sure no one else has claimed
it first.

## How to contribute (and coordinate effort)
So (for now), the workflow looks like this:

1. Identify a feature, bug, etc to work on
2. Check to see if an issue has already been created
3. If it hasn't been created yet, create the issue and wait to discuss before
starting work
4. If it has been created, check to see if it has been claimed. If it isn't
immediately apparent that someone is already working on it, comment to find
out. If it has, please let the other person continue work (or offer to help 
if appropriate).

## Branch Structure
I'm working my way towards a more traditional GitFlow.
- `main` is the primary branch. Only fully-functional PRs should be opened to main.
- `production` is the production branch. It should never be pushed to directly, and
PRs should only be opened from `main`. Any commits/PRs are automatically and
immediately deployed.
- `feature-[*]` Branches with "feature" prepended are feature branches. Most work
happens in these.
- I'm really hoping we never need a `hotfix`, but if we do, we'll make it then.
