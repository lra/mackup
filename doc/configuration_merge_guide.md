# Guide for Merging Configurations Across Machines

This guide is for users who want to combine configuration
settings for two or more machines.

For example, you might have some bash settings
on Machine A (like useful command aliases) that are not on Machine B.
You also have some settings on Machine B that you would live to move
over to Machine A.

The problem is that if you use Mackup to send Machine A's bash configuration
settings to Machine B, you will permanently lose any configurations on
Machine B that you wanted to keep. Mackup obviously has no idea which features
you want to keep and which ones you don't so you'll have to do a little bit of work
to merge the different configuration files yourself before using Mackup.

## Step 0: Read Through This Entire Guide First

It will probably save you some pain in the long run.

## Step 1: Determine Which Configuration Files to Merge

First, pick the app you wish to keep in sync. Then
determine which configuration files will be synced for that application by doing
the following:

1. [Install Mackup](INSTALL.md)
1. Create a `.mackup.cfg` file in your home directory
1. Add the following two lines to `.mackup.cfg`:

```
[applications_to_sync]
<replace_this_line_the_name_of_the_app>
```

You can get a list of supported apps by running `mackup list`.

1. Save the file
1. Run the following command:

`mackup --dry-run --verbose backup`

This command will let you see what mackup will do behind the scenes when
it backs up your application's configuration files so you can readily see what
configuration files Mackup will sync. Make note of these files.

## Step 2: Prepare Your Servers to Sync

Now that you've identified which files you have to merge, choose one of the two
approaches below for merging the configuration files. Method 1 has you do all
the configuration file merges first and then pushes out them out with Mackup.
With Method 2, you'll push out the configuration files from one machine to the
others and then merge in your configuration changes gradually over time. Method
1 is more work up front in exchange for less work later. Method 2 is less work
up front but more work later. Method 1 is probably best if you have very
dissimilar configurations and have few machines. Method 2 is probably best if
you have a machine that is very close to working the way you want and just need
some minor tweaks from other machines.

### Method 1: Backup/Merge/Push Approach

1. Create a backup of each machine's configuration files for the app you wish to sync.
1. Choose a machine that will serve as the initial "master". It doesn't really matter which one.
1. For each configuration file you wish to sync, create a new file that represents the ideal version of the file you wish to distribute out to your other machines.
1. Replace the files on the master with the configuration files created in step 2.

### Method 2: Backup/Push/Merge Approach

1. Choose a machine that will serve as the initial "master". You'll probably want to use choose the machine you use most and like its configuration settings the best.
1. For each machine that aren't the "master" (i.e. "slaves"), back up all the configuration files for each app that you want to sync. That's it for now. However, there will be more work for you later.

## Step 3: Push Out the Configuration Files with Mackup

Now you are ready to use Mackup to push out the changes. You should have Mackup already
installed and the `.mackup.cfg` file in place according to the instructions provided
above. If not, do that before proceeding.

Run the following command on the master machine:

`mackup backup`

On each of the other "slave" machines, run:

`mackup restore`

If you used Method 1 in Step 2 above, you are done. If you used Method 2, you'll
need to merge in new features over time. As you discover features you need to
add, you'll need to taked the appropriate snippets of code from the backup
configuration files you created and insert them to the appropriate configuration
file. Remember it does not matter which machine's configuration file you update
as these configuration files are now shared across all machines.
