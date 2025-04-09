import pygame


events: list[pygame.event.Event] = []


def update() -> None:
	global events
	events = pygame.event.get()


def get() -> list[pygame.event.Event]:
	return events
