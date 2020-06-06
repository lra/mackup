# Guide for Merging Configurations Across Machines

This guide is for users who want to combine configuration settings for two or
more machines.

For example, you might have some bash settings on Machine A (like useful
command aliases) that are not on Machine B.  You also have some settings on
Machine B that you would live to move over to Machine A.

The problem is that if you use Mackup to send Machine A's bash configuration
settings to Machine B, you will permanently lose any configurations on Machine
B that you wanted to keep. Mackup obviously has no idea which features you want
to keep and which ones you don't so you'll have to do a little bit of work to
merge the different configuration files yourself before using Mackup.

## Step 0: Read Through This Entire Guide First

It will probably save you some pain in the long run.

## Step 1: Determine Which Configuration Files to Merge

First, pick the app you wish to keep in sync. Then determine which
configuration files will be synced for that application by doing the following:

1. [Install Mackup](./../INSTALL.md)
1. Create a `.mackup.cfg` file in your home directory
1. Add the following two lines to `.mackup.cfg`. Replace **bash**
   in the example below with the name of your application.

```
[applications_to_sync]
bash
```

You can get a list of supported apps by running `mackup list`.

1. Save the file
1. Run the following command:

`mackup --dry-run --verbose backup`

This command will let you see what mackup will do behind the scenes when it
backs up your application's configuration files so you can readily see what
configuration files Mackup will sync. Make note of these files.

## Step 2: Prepare Your Workstations for Syncing

Now that you've identified which files you have to merge, choose one of the two
approaches below for merging the configuration files. **Method 1** has you do all
the configuration file merges first and then pushes out them out with Mackup.
With **Method 2**, you'll push out the configuration files from one machine to the
others and then merge in your configuration changes gradually over time.

Which method should you use? It doesn't really matter. Method 1 is more work up
front in exchange for less work later. Method 2 is less work up front but more
work later.

Method 1 is probably best if you have very dissimilar configurations and have
few machines. Method 2 is probably best if you have a machine that is very
close to working the way you want and just need a few configuration settings
from other machines.

### Method 1: Backup Merge-Push Approach

1. Create a backup of each machine's configuration files for the app you wish
   to sync.
1. Choose a machine that will serve as the initial "master". It doesn't really
   matter which one.
1. Edit your configuration files on the master machine so that they
   represent the ideal version of the file you wish to distribute out to your
   other machines.

#### Method 1 Example

Let's say we have two machines, A and B and that we want to sync our bash configuration
across the machines. We decide that Machine A will serve as our master.

First, backup the bash configuration files (there are a few of them)
for your application on all machines.

##### Sample backup commands for Machine A**

```
mkdir ~/bash_backup
cp ~/.bash_profile ~/bash_backup/bash_profile.bak
cp ~/.bash_login ~/bash_backup/bash_login.bak

...plus any other bash config files you want to keep
```

##### Sample backup commands for Machine B

```
mkdir ~/bash_backup
cp ~/.bash_profile ~/bash_backup/bash_profile.bak
cp ~/.bash_login ~/bash_backup/bash_login.bak

...plus any other bash config files you want to keep
```

Machine A will be our master so we now edit the existing configuration files
on Machine A. We will use the vim text editor to do this for each of our
configuration files:

```
vim .bash_profile
vim .bash_login
```

When editing these configuration files on Machine A, copy and and paste the settings
from Machine B that you want to keep. In essence, you are manually merging the
configuratoin files together. Once you are satisfied the configuration files
have all the settings you want and need, you are ready to push out your changes from
the master machine.

### Method 2: Backup Push-Merge Approach

1. Choose a machine that will serve as the initial "master". You'll probably
   want to use choose the machine you use most and like its configuration
   settings the best.
1. For each machine that aren't the "master" (i.e. "slaves"), back up all the
   configuration files for each app that you want to sync. That's it for now.
   However, there will be more work for you later.

#### Method 2 Example

Let's say we have two machines, A and B and that we want to sync our bash configuration
across the machines. We decide that Machine A will serve as our master.

Since A is our master, we only need to backup the bash configuration files on
Machine B:

##### Sample backup commands for Machine B**

```
mkdir ~/bash_backup
cp ~/.bash_profile ~/bash_backup/bash_profile.bak
cp ~/.bash_login ~/bash_backup/bash_login.bak

...plus any other bash config files you want to keep
```

If you have other machines you are syncing with the master, back those up, woo.

## Step 3: Push Out the Configuration Files with Mackup

Now you are ready to use Mackup to push out the changes. You should have Mackup
already installed and the `.mackup.cfg` file in place according to the
instructions provided above. If not, do that before proceeding.

Run the following command on the master machine:

`mackup backup`

On each of the other "slave" machines, run:

`mackup restore`

If you used Method 1 in Step 2 above, you are done. You may you discover
that you didn't quite merge the files exactly the way you wanted but don't
worry, that's why you created the configuration file backups. You can grab
snippets from these backup configuration files and add them in to the live
configuraton files and then easily push the changes out to all your
machines using mackup.

If you used Method 2, you'll need to merge in new features over time. As you
discover features you need to add, you'll need to take the appropriate snippets
of configuration code from the backup configuration files you created and
insert them into the appropriate configuration file. Remember it does not matter
which machine's configuration file you update as these configuration files are
now shared across all machines.
