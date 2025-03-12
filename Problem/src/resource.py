# src/resource.py
"""
Defines the Resource class, which encapsulates the properties and lifecycle
of a resource in the challenge.
"""

class Resource:
    def __init__(self, resource_def):
        """
        Initialize a resource instance from its definition.
        resource_def: dictionary with keys:
            'id', 'activation_cost', 'periodic_cost', 'active_duration',
            'downtime', 'lifecycle', 'buildings_powered', 'resource_type', 'special_effect'
        """
        self.id = resource_def['id']
        self.activation_cost = resource_def['activation_cost']
        self.periodic_cost = resource_def['periodic_cost']
        self.active_duration = resource_def['active_duration']
        self.downtime = resource_def['downtime']
        self.lifecycle = resource_def['lifecycle']
        self.buildings_powered = resource_def['buildings_powered']
        self.resource_type = resource_def['resource_type']
        self.special_effect = resource_def['special_effect']
        
        # Internal state for simulation:
        self.turns_elapsed = 0  # Total number of turns this resource has been used
        self.state = 'active'   # Current state: 'active' or 'downtime'
        self.state_remaining = self.active_duration  # Turns remaining in the current state

    def update_state(self):
        """
        Update the resource state at the end of the turn.
        Returns:
          True if the resource is still alive, False if it has expired.
        """
        self.turns_elapsed += 1
        self.state_remaining -= 1
        
        if self.turns_elapsed >= self.lifecycle:
            # Resource has reached its end-of-life.
            return False
        
        if self.state_remaining == 0:
            # Switch state.
            if self.state == 'active':
                self.state = 'downtime'
                self.state_remaining = self.downtime
            else:
                self.state = 'active'
                remaining_life = self.lifecycle - self.turns_elapsed
                self.state_remaining = min(self.active_duration, remaining_life)
        return True

    def is_active(self):
        """
        Check if the resource is active (i.e., providing power) in the current turn.
        """
        return self.state == 'active'

    def get_power(self):
        """
        Return the number of buildings powered by this resource during this turn.
        """
        if self.is_active():
            return self.buildings_powered
        return 0

    def get_maintenance_cost(self):
        """
        Return the maintenance cost of the resource for the current turn.
        """
        return self.periodic_cost
