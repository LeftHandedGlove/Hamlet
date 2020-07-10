echo "Creating hamlet user"
useradd -m hamlet

echo "Enter new password for hamlet user"
passwd hamlet

echo "Copying pi user's groups"
entry_count=0
for group in $(groups pi); do
	entry_count=$((entry_count+1))
    if [ $entry_count -gt 3 ]; then
	echo "  Adding hamlet to group $group"
        usermod -a -G $group hamlet
    fi
done

echo "Reboot the Raspberry Pi, login as 'hamlet', and delete the 'pi' user with 'userdel -r pi'"
