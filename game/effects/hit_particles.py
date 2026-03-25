"""
Simple particle effect for when projectiles hit enemies.
Creates a blood splash effect using Ursina's Entity system.
"""
from ursina import Entity, color, destroy, time, Vec3, random
import random as py_random

def create_hit_effect(position, hit_color=color.red):
    """
    Creates a simple particle splash effect at the hit position.
    
    Args:
        position: Vec3 position where the hit occurred
        hit_color: Color of the particles (default red for blood)
    """
    num_particles = 8
    particles = []
    
    for i in range(num_particles):
        # Random direction for each particle
        direction = Vec3(
            py_random.uniform(-1, 1),
            py_random.uniform(0.5, 1.5),  # Mostly upward
            py_random.uniform(-1, 1)
        ).normalized()
        
        speed = py_random.uniform(2, 5)
        
        particle = Entity(
            model='sphere',
            color=hit_color,
            scale=0.15,
            position=position,
            collider=None
        )
        
        # Store particle data
        particle.velocity = direction * speed
        particle.lifetime = py_random.uniform(0.3, 0.6)
        particle.age = 0
        particles.append(particle)
    
    # Update and cleanup particles
    def update_particles():
        for particle in particles[:]:  # Copy list to safely remove items
            if not particle:
                continue
                
            particle.age += time.dt
            
            # Apply gravity
            particle.velocity.y -= 9.8 * time.dt
            
            # Move particle
            particle.position += particle.velocity * time.dt
            
            # Fade out
            alpha = 1 - (particle.age / particle.lifetime)
            particle.alpha = max(0, alpha)
            
            # Shrink
            scale_factor = 1 - (particle.age / particle.lifetime)
            particle.scale = 0.15 * scale_factor
            
            # Destroy when lifetime is over
            if particle.age >= particle.lifetime:
                destroy(particle)
                particles.remove(particle)
        
        # Stop updating when all particles are gone
        if not particles:
            return False  # Signal to stop updating
        return True  # Continue updating
    
    # Create updater entity
    updater = Entity()
    updater.update = update_particles
    
    # Auto-destroy updater after max lifetime
    destroy(updater, delay=1.0)
    
    return particles


def create_simple_hit_effect(position, hit_color=color.red):
    """
    Simpler hit effect - just a quick flash.
    More performant for many simultaneous hits.
    """
    flash = Entity(
        model='sphere',
        color=hit_color,
        scale=0.5,
        position=position,
        collider=None
    )
    
    # Animate scale and alpha
    flash.animate_scale(0, duration=0.3, curve=lambda t: 1-t)
    flash.animate('alpha', 0, duration=0.3)
    
    # Auto-destroy
    destroy(flash, delay=0.3)
    
    return flash
