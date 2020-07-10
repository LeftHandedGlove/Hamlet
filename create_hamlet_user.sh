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

echo "The hamlet user has been created! Please perform the following:"
echo "1) Disable auto-login as pi using 'sudo raspi-config'"
echo "2) Reboot the Raspberry Pi using 'sudo reboot'"
echo "3) Login as hamlet"
echo "4) Delete the 'pi' user with 'userdel -r pi'"
